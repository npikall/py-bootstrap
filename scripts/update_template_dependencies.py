import logging
import re
from dataclasses import dataclass
from enum import Enum, auto
from functools import lru_cache
from pathlib import Path

import httpx

log = logging.getLogger(__name__)


class Resolver(Enum):
    PYPI = auto()
    GITHUB = auto()


class Formatting(Enum):
    DEFAULT = auto()
    UPPER_BOUND = auto()
    MAJOR_ONLY = auto()
    GITHUB_ACTION = auto()
    SIMPLE = auto()


@dataclass(frozen=True)
class DependencyRule:
    file_glob: str
    package: str
    pattern: str
    resolver: Resolver
    formatter: Formatting = Formatting.DEFAULT


def pattern_greater_equal_semver(package: str) -> str:
    return rf"\"{package}>=([0-9]*.[0-9]*.[0-9]*)\""


RULES = [
    DependencyRule(
        file_glob="**/pyproject.toml.jinja",
        package="pytest",
        pattern=pattern_greater_equal_semver("pytest"),
        resolver=Resolver.PYPI,
    ),
    # TODO: missing PyTest-cov  # noqa: FIX002
    DependencyRule(
        file_glob="**/pyproject.toml.jinja",
        package="ruff",
        pattern=pattern_greater_equal_semver("ruff"),
        resolver=Resolver.PYPI,
    ),
    DependencyRule(
        file_glob="**/pyproject.toml.jinja",
        package="ty",
        pattern=pattern_greater_equal_semver("ty"),
        resolver=Resolver.PYPI,
    ),
    DependencyRule(
        file_glob="**/pyproject.toml.jinja",
        package="mkdocstrings-python",
        pattern=pattern_greater_equal_semver("mkdocstrings-python"),
        resolver=Resolver.PYPI,
    ),
    DependencyRule(
        file_glob="**/pyproject.toml.jinja",
        package="zensical",
        pattern=pattern_greater_equal_semver("zensical"),
        resolver=Resolver.PYPI,
    ),
    DependencyRule(
        file_glob="**/pyproject.toml.jinja",
        package="uv-build",
        pattern=r"\"uv-build>=([0-9]*.[0-9]*.[0-9]*),<[0-9]*.[0-9]*\"",
        resolver=Resolver.PYPI,
        formatter=Formatting.UPPER_BOUND,
    ),
    DependencyRule(
        file_glob="**/*.github*/workflows/*docs.yml*",
        package="actions/configure-pages",
        pattern=r"actions/configure-pages@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/workflows/*.yml*.jinja",
        package="actions/checkout",
        pattern=r"actions/checkout@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/workflows/*docs.yml*",
        package="actions/setup-python",
        pattern=r"actions/setup-python@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/workflows/*docs.yml*",
        package="actions/upload-pages-artifact",
        pattern=r"actions/upload-pages-artifact@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/workflows/*docs.yml*",
        package="actions/deploy-pages",
        pattern=r"actions/deploy-pages@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/**/*.yml*",
        package="astral-sh/setup-uv",
        pattern=r"astral-sh/setup-uv@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/workflows/*test_coverage.yml*",
        package="py-cov-action/python-coverage-comment-action@v3",
        pattern=r"py-cov-action/python-coverage-comment-action@v[0-9]*",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,
    ),
    DependencyRule(
        file_glob="**/*.github*/actions/setup/action.yml",
        package="astral-sh/uv",
        pattern=r"version: \"([0-9]*.[0-9]*.[0-9]*)\"",
        resolver=Resolver.GITHUB,
        formatter=Formatting.GITHUB_ACTION,  # TODO: needs another formatter
    ),
]


def main() -> None:
    setup_logging()
    root = get_project_root()
    for rule in RULES:
        process_rule(rule, root / "template")


def process_rule(rule: DependencyRule, root: Path) -> None:
    files = root.rglob(rule.file_glob)
    for file in files:
        process_file(rule, file)


def process_file(rule: DependencyRule, file: Path) -> None:
    log.debug("process file: %s, exists: %s", file.name, file.is_file())
    pattern = re.compile(rule.pattern)
    current = get_current_version(pattern, file.read_text())
    if current is None:
        log.debug("current not found in %s for %s", file.name, rule.package)
        return
    latest = fetch_latest_version(rule)
    if latest is None:
        log.debug("latest not found for %s", rule.package)
        return
    if current != latest:
        apply_update_to_file(rule, file, current, latest)
    else:
        log.info("package %s already at latest version", rule.package)


def apply_update_to_file(
    rule: DependencyRule,
    file: Path,
    current: str,
    latest: str,
) -> None:
    log.info("update %s in %s: %s -> %s", rule.package, file.name, current, latest)
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
        log.warning("no match found for pattern: %s", pattern)
        return None
    if len(matched_stmts) > 1:
        log.warning("multiple matches found: %s", matched_stmts)
    sorted_versions: list[str] = sorted(matched_stmts, reverse=True)
    return sorted_versions[0]


def fetch_latest_version(rule: DependencyRule) -> str | None:
    log.debug("fetching latest for %s", rule.package)
    match rule.resolver:
        case Resolver.PYPI:
            return fetch_latest_version_from_pypi(rule.package)
        case Resolver.GITHUB:
            return fetch_latest_version_from_github(rule.package)


@lru_cache(maxsize=128)
def fetch_latest_version_from_pypi(package: str) -> str | None:
    resp = httpx.get(f"https://pypi.org/pypi/{package}/json", timeout=10)
    if resp.status_code != httpx.codes.OK:
        return None
    return resp.json().get("info", {}).get("version")


@lru_cache(maxsize=128)
def fetch_latest_version_from_github(repo: str) -> str | None:
    resp = httpx.get(f"https://api.github.com/repos/{repo}/releases/latest", timeout=10)
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
    log.setLevel(logging.INFO)


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
