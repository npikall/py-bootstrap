import re
from datetime import datetime
from pathlib import Path
from typing import Any, TypedDict

import yaml

COPIER_CONFIG_PATH: Path = Path(__file__).resolve().parent.parent / "copier.yml"
COPIER_CONFIG: dict[Any, Any] = yaml.safe_load(COPIER_CONFIG_PATH.read_text())

PY_VERSION: str = COPIER_CONFIG["py_version_current"]["default"]
PY_VERSION_PAST: str = COPIER_CONFIG["py_version_past"]["default"]
PY_VERSION_FUTURE: str = COPIER_CONFIG["py_version_future"]["default"]
CUR_YEAR: int = datetime.today().year  # noqa: DTZ002


def get_lines(start: int, end: int, content: str) -> str:
    return "\n".join(content.splitlines()[start:end])


class Cases(TypedDict):
    """Struct for table-driven tests"""

    want: str
    start: int
    end: int


def get_linenumbers_to_delete_in_justfile(content: str) -> tuple[int, int]:
    result = re.findall(r"sed\s+'([^']+)'", content)[0]
    assert isinstance(result, str)
    result = result.rstrip("d")
    parts = result.split(",")
    return int(parts[0]), int(parts[1])


def test_copier_links_all_files_correct(copied_project: Path):
    want: list[str] = [
        # DOTFILES
        ".gitignore",
        ".python-version",
        ".pre-commit-config.yaml",
        ".gitlab-ci.yml",
        # REGULAR FILES
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "Justfile",
        "init.just",
        "README.md",
        "pyproject.toml",
        "LICENSE",
        "zensical.toml",
        # SRC DIRECTORY
        "src/example/__init__.py",
        "src/example/py.typed",
        # TEST DIRECTORY
        "tests/smoke_test.py",
        "tests/test_meta.py",
        # DOCS DIRECTORY
        "docs/index.md",
        "docs/license.md",
        "docs/contributing.md",
        "docs/changelog.md",
        "docs/reference/api.md",
        # GITHUB DIRECTORY
        ".github/actions/setup/action.yml",
        ".github/ISSUE_TEMPLATE/1-bug.md",
        ".github/ISSUE_TEMPLATE/2-feature.md",
        ".github/ISSUE_TEMPLATE/3-docs.md",
        ".github/ISSUE_TEMPLATE/4-change.md",
        ".github/workflows/code_quality.yml",
        ".github/workflows/docs.yml",
        ".github/workflows/publish.yml",
        ".github/workflows/release.yml",
        ".github/workflows/test_coverage.yml",
        ".github/workflows/test_platform.yml",
        # COPIER METADATA
        ".copier-answers.yml",
    ]

    # Check all expected files get copied
    for file in want:
        assert (copied_project / file).exists()

    # Check if more than expected number of files got copied
    for file in copied_project.rglob("*"):
        if file.is_dir():
            continue
        rel_path = str(file.relative_to(copied_project))
        assert rel_path in want


def test_readme_renders_correct(copied_project: Path):
    got = (copied_project / "README.md").read_text()
    want = "# example"
    assert want in got


def test_pyproject_toml_renders_correct(copied_project: Path):
    got = (copied_project / "pyproject.toml").read_text()
    cases = [
        '[project]\nname = "example"',
        'authors = [ { name = "John Doe", email = "john.doe@mail.com" } ]',
        "mkdocstrings-python>=",
        "zensical>=",
        'addopts = "--cov=example',
        "- {% if commit.scope %}_({{ commit.scope }})_ {% endif %}",
        r'{ message = "^chore\\(release\\): bump version to", skip = true },',
    ]
    for want in cases:
        assert want in got


def test_python_version_renders_correct(copied_project: Path):
    got = (copied_project / ".python-version").read_text()
    want = PY_VERSION
    assert want in got


def test_contributing_renders_correct(copied_project: Path):
    got = (copied_project / "CONTRIBUTING.md").read_text()
    cases: list[str] = [
        "Report bugs at [`github.com/jdoe/example`][repo].",
        "`example` could always use more documentation",
    ]
    for want in cases:
        assert want in got


def test_justfile_renders_correct(copied_project: Path):
    got = (copied_project / "Justfile").read_text()
    cases: list[str] = [
        f"uv run --python={PY_VERSION} pytest {{{{ args }}}}",
        "\nhooks:\n    uvx prek run --all-files\n\n#",
        "\nhooks-install:\n    uvx prek install\n\n#",
        "    uv run zensical serve\n\n",
        f'ci python="{PY_VERSION}":\n    uv',
        r"uv run --python={{ python }} ruff format .",
        r"uv run pytest tests/ {{ args }}",
        r"uvx git-cliff -o {{ args }}",
        "@just changelog --tag `uv version --short`",
    ]
    for t in cases:
        assert t in got


def test_gitlab_ci_renders_correct(copied_project: Path):
    got = (copied_project / ".gitlab-ci.yml").read_text()
    want = f'PYTHON_VERSION: "{PY_VERSION}"'
    assert want in got


def test_license_MIT_renders_correct(copied_project: Path):  # noqa: N802
    got = (copied_project / "LICENSE").read_text()
    want = f"Copyright (c) {CUR_YEAR} John Doe"
    assert want in got


def test_zensical_renders_correct(copied_project: Path):
    got = (copied_project / "zensical.toml").read_text()
    cases: list[str] = [
        'site_name = "Example - Documentation"',
        'site_author = "John Doe"',
        f'copyright = """\nCopyright &copy; {CUR_YEAR} John Doe\n"""',
        'media = "(prefers-color-scheme)"',
        'media = "(prefers-color-scheme: light)"',
        'media = "(prefers-color-scheme: dark)"',
    ]
    for want in cases:
        assert want in got


def test_test_platform_renders_correct(copied_project: Path):
    got = (copied_project / ".github/workflows/test_platform.yml").read_text()
    want_1 = (
        "python-version:\n"
        f'          - "{PY_VERSION_PAST}"\n'
        f'          - "{PY_VERSION}"\n'
        f'          - "{PY_VERSION_FUTURE}"'
    )
    assert want_1 in got


def test_test_coverage_renders_correct(copied_project: Path):
    got = (copied_project / ".github/workflows/test_coverage.yml").read_text()
    want = "GITHUB_TOKEN: ${{ github.token }}"
    assert want in got


def test_publish_renders_correct(copied_project: Path):
    got = (copied_project / ".github/workflows/publish.yml").read_text()
    want = f"run: uv python install {PY_VERSION}"
    assert want in got


def test_init_just_deletes_correct_content_in_justfile(copied_project: Path):
    init_just_content = (copied_project / "init.just").read_text()
    just_content = (copied_project / "Justfile").read_text()
    start_line, end_line = get_linenumbers_to_delete_in_justfile(init_just_content)
    got = get_lines(start_line, end_line, just_content)
    want = 'import? "init.just"'
    assert got == want


def test_release_action_renders_correctly(copied_project: Path):
    got = (copied_project / ".github/workflows/release.yml").read_text()
    want = "uses: taiki-e/install-action@git-cliff"
    assert want in got
