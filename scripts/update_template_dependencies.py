import asyncio
import logging
import re
from enum import StrEnum, auto
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Any

import httpx
from pydantic import BaseModel, TypeAdapter

if TYPE_CHECKING:
    from types import CoroutineType

log = logging.getLogger(__name__)


type VersionMapping = dict[str, str | None]


class Resolver(StrEnum):
    PYPI = auto()
    GITHUB = auto()


class Formatting(StrEnum):
    DEFAULT = auto()
    UPPER_BOUND = auto()
    MAJOR_ONLY = auto()
    GITHUB_ACTION = auto()
    SIMPLE = auto()


class DependencyRule(BaseModel):
    file_glob: str
    package: str
    pattern: str
    resolver: Resolver
    formatter: Formatting = Formatting.DEFAULT


def main() -> None:
    setup_logging()
    rules = load_rules()
    root = get_project_root()
    template_dir = root / "template"
    latest_versions = collect_latest_versions(rules)
    for rule in rules:
        process_rule(rule, template_dir, latest_versions)


def load_rules() -> list[DependencyRule]:
    json_file = Path(__file__).parent / "dependency_rules.json"
    rules_model = TypeAdapter(list[DependencyRule])
    return rules_model.validate_json(json_file.read_bytes())


def process_rule(
    rule: DependencyRule, root: Path, fetched_versions: VersionMapping
) -> None:
    files = root.rglob(rule.file_glob)
    for file in files:
        process_file(rule, file, fetched_versions)


def process_file(
    rule: DependencyRule, file: Path, fetched_versions: VersionMapping
) -> None:
    log.debug(
        "process file: %s, exists: %s",
        remove_jinja_tags_from_filename(file.name),
        file.is_file(),
    )
    versions = get_latest_and_current_versions_if_available(
        rule, file, fetched_versions
    )
    if versions is None:
        return
    current, latest = versions
    if current != latest:
        apply_update_to_file(rule, file, current, latest)
    else:
        log.info("package %s already at latest version", rule.package)


def remove_jinja_tags_from_filename(name: str) -> str:
    jinja_tags = re.compile(r"({%.*?%}|{{.*?}}|{#.*?#})")
    return jinja_tags.sub("", name)


def get_latest_and_current_versions_if_available(
    rule: DependencyRule, file: Path, fetched_versions: VersionMapping
) -> tuple[str, str] | None:
    pattern = re.compile(rule.pattern)
    current = get_current_version(pattern, file.read_text())
    if current is None:
        log.debug(
            "current not found in %s for %s",
            remove_jinja_tags_from_filename(file.name),
            rule.package,
        )
        return None
    latest = fetched_versions.get(rule.package)
    if latest is None:
        log.debug("latest not found for %s", rule.package)
        return None
    return current, latest


def apply_update_to_file(
    rule: DependencyRule,
    file: Path,
    current: str,
    latest: str,
) -> None:
    log.info(
        "update %s in %s: %s -> %s",
        rule.package,
        remove_jinja_tags_from_filename(file.name),
        current,
        latest,
    )
    pattern = re.compile(rule.pattern)
    replacement = format_version_replacement(rule, latest)
    update_file(file, pattern, replacement)


def update_file(file: Path, pattern: re.Pattern, repl: str) -> None:
    new_content = update_file_content(file, pattern, repl)
    file.write_text(new_content)


@lru_cache(maxsize=128)
def get_next_minor_version(version: str) -> str:
    parts = version.split(".")
    minor = str(int(parts[1]) + 1)
    return f"{parts[0]}.{minor}"


def format_version_replacement(rule: DependencyRule, version: str) -> str:
    match rule.formatter:
        case Formatting.GITHUB_ACTION:
            latest_major = version.split(".", maxsplit=1)[0].lstrip("v")
            return f"{rule.package}@v{latest_major}"
        case Formatting.UPPER_BOUND:
            upper = get_next_minor_version(version)
            return format_dependency_string_with_upper(rule.package, version, upper)
        case Formatting.MAJOR_ONLY:
            major = version.split(".", maxsplit=1)[0].lstrip("v")
            return format_dependency_string(rule.package, major)
        case Formatting.DEFAULT:
            return format_dependency_string(rule.package, version)
        case Formatting.SIMPLE:
            return f'version: "{version}"'


def format_dependency_string(package: str, version: str) -> str:
    return f'"{package}>={version}"'


def format_dependency_string_with_upper(package: str, version: str, upper: str) -> str:
    return f'"{package}>={version},<{upper}"'


def update_file_content(file: Path, pattern: re.Pattern[str], repl: str) -> str:
    return pattern.sub(repl, file.read_text())


def get_current_version(pattern: re.Pattern, content: str) -> str | None:
    matched_stmts = pattern.findall(content)
    if not matched_stmts:
        log.debug("no match found for pattern: %s", pattern)
        return None
    if len(matched_stmts) > 1:
        log.warning("multiple matches found: %s", matched_stmts)
    sorted_versions: list[str] = sorted(matched_stmts, reverse=True)
    return sorted_versions[0]


def collect_latest_versions(rules: list[DependencyRule]) -> VersionMapping:
    latest_versions: VersionMapping = {}
    all_versions = asyncio.run(fetch_all_latest_versions(rules))
    for package, version in all_versions:
        latest_versions[package] = version
    return latest_versions


async def fetch_all_latest_versions(
    rules: list[DependencyRule],
) -> list[tuple[str, str | None]]:
    async with httpx.AsyncClient() as client:
        tasks: list[CoroutineType[Any, Any, tuple[str, str | None]]] = [
            fetch_latest_version(rule, client) for rule in rules
        ]
        return await asyncio.gather(*tasks)


async def fetch_latest_version(
    rule: DependencyRule, client: httpx.AsyncClient
) -> tuple[str, str | None]:
    log.debug("fetching latest for %s", rule.package)
    match rule.resolver:
        case Resolver.PYPI:
            latest = await fetch_latest_version_from_pypi(rule.package, client)
            return rule.package, latest
        case Resolver.GITHUB:
            latest = await fetch_latest_version_from_github(rule.package, client)
            return rule.package, latest


@lru_cache(maxsize=128)
async def fetch_latest_version_from_pypi(
    package: str, client: httpx.AsyncClient
) -> str | None:
    url = f"https://pypi.org/pypi/{package}/json"
    resp = await client.get(url, timeout=10)
    if resp.status_code != httpx.codes.OK:
        return None
    return resp.json().get("info", {}).get("version")


@lru_cache(maxsize=128)
async def fetch_latest_version_from_github(
    repo: str, client: httpx.AsyncClient
) -> str | None:
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    resp = await client.get(url, timeout=10)
    if resp.status_code != httpx.codes.OK:
        return None
    return resp.json().get("tag_name", "")


def setup_logging() -> None:
    logging.basicConfig(
        format="{asctime} {levelname} {message}",
        style="{",
        datefmt="%Y/%m/%d %H:%M:%S",
        level=logging.INFO,
    )
    log.setLevel(logging.WARNING)


def get_project_root(root_marker_file: str = "pyproject.toml") -> Path:
    current_filepath = Path(__file__)
    for parent in current_filepath.parents:
        if (parent / root_marker_file).exists():
            log.debug("root: %s", parent)
            return parent
    err = f"no '{root_marker_file}' found in any parent directories"
    raise FileNotFoundError(err)


if __name__ == "__main__":
    main()
