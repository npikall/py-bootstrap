import re
from collections.abc import Iterable
from pathlib import Path

import yaml

CWD = Path(__file__).parent.parent
JINJA_VARIABLE = r"{{.[a-zA-Z0-9\s]*.}}"

EXTEND_ALLOW = [
    "PYTHON",
    "PROJ",
    "INCREMENT",
    "VERSION",
    "GREEN",
    "BOLD",
    "NORMAL",
]


def load_copier_variables() -> list[str]:
    config_file = CWD / "copier.yml"
    config = yaml.safe_load(config_file.read_text())
    variables: list[str] = config.keys()
    return [v for v in variables if not v.startswith("_")]


def scan_file(path: Path) -> set[str]:
    content: str = path.read_text()
    raw: list[str] = re.findall(pattern=JINJA_VARIABLE, string=content)
    return {v.strip("{} ") for v in raw}


def check_jinja_tag_is_valid(tag: str, allowed: list[str]) -> bool:
    return tag in allowed


def check_variables(candidates: Iterable[str], allowed: list[str]) -> str | None:
    for candidate in candidates:
        if not check_jinja_tag_is_valid(tag=candidate, allowed=allowed):
            return candidate
    return None


def test_only_valid_jinja_tags_used():
    config = load_copier_variables()
    config.extend(EXTEND_ALLOW)
    template_dir = CWD / "template"
    for file in template_dir.iterdir():
        if file.is_dir():
            continue
        scan_variables = scan_file(file)
        checked = check_variables(candidates=scan_variables, allowed=config)
        assert checked is None, f"unexpected tag: {checked}"
