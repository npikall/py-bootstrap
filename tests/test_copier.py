from datetime import datetime
from pathlib import Path
from typing import TypedDict

import pytest
from conftest import FullUserAnswers as UserAnswers
from copier import run_copy

# NOTE: Keep synced with 'copier.yml'
PY_VERSION = "3.12"
PY_VERSION_PAST = "3.10"
PY_VERSION_FUTURE = "3.14"
CUR_YEAR = datetime.today().year  # noqa: DTZ002


def get_lines(start: int, end: int, content: str) -> str:
    return "\n".join(content.splitlines()[start:end])


class Cases(TypedDict):
    """Struct for table-driven tests"""

    want: str
    start: int
    end: int


@pytest.fixture(scope="session")
def session_tmp_path(tmp_path_factory):
    return tmp_path_factory.mktemp("main")


def test_copier_links_all_files_correct(
    session_tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = UserAnswers()
    cwd = Path(__file__).resolve().parent.parent

    # Run copier with the given context
    run_copy(
        src_path=str(cwd),
        dst_path=session_tmp_path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()

    want: list[str] = [
        # DOTFILES
        ".gitignore",
        ".python-version",
        ".pre-commit-config.yaml",
        ".gitlab-ci.yml",
        ".goreleaser.yaml",
        # REGULAR FILES
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "Justfile",
        "README.md",
        "pyproject.toml",
        "LICENSE",
        "zensical.toml",
        # SRC DIRECTORY
        "src/example/__init__.py",
        # TEST DIRECTORY
        "tests/smoke_test.py",
        "tests/test_meta.py",
        # DOCS DIRECTORY
        "docs/index.md",
        # GITHUB DIRECTORY
        ".github/actions/setup/action.yml",
        ".github/workflows/code_quality.yml",
        ".github/workflows/docs.yml",
        ".github/workflows/publish.yml",
        ".github/workflows/test_coverage.yml",
        ".github/workflows/test_platform.yml",
        # COPIER METADATA
        ".copier-answers.yml",
    ]

    # Check all expected files get copied
    for file in want:
        assert (session_tmp_path / file).exists()

    # Check if more than expected number of files got copied
    for file in session_tmp_path.iterdir():
        if file.is_dir():
            continue
        rel_path = str(file.relative_to(session_tmp_path))
        assert rel_path in want


def test_readme_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "README.md").read_text()
    want = "# example"
    assert want in got


def test_pyproject_toml_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "pyproject.toml").read_text()
    want_1 = """[project]
authors = [{ name = "John Doe", email = "john.doe@mail.com" }]
name = "example"
"""
    want_2 = '\ndocs = [\n    "zensical>=0.0.11",\n    "mkdocstrings-python>=2.0.1",\n]'
    want_3 = 'addopts = "--cov=example'
    assert want_1 in got
    assert want_2 in got
    assert want_3 in got


def test_python_version_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / ".python-version").read_text()
    want = PY_VERSION
    assert want in got


def test_contributing_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "CONTRIBUTING.md").read_text()
    cases: list[str] = [
        "Report bugs at https://github.com/jdoe/example/issues.",
        "example could always use more documentation",
    ]
    for want in cases:
        assert want in got


def test_justfile_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "Justfile").read_text()
    cases: list[Cases] = [
        # Want Rendering
        {"want": f"uv run --python={PY_VERSION} pytest", "start": 36, "end": 40},
        {"want": "\nhooks:\n    uvx prek install\n\n#", "start": 48, "end": 53},
        {"want": "    uv run zensical serve\n\n# initialize", "start": 113, "end": 119},
        # No Rendering
        {"want": r"uv run --python={{ PYTHON }} ruff format .", "start": 42, "end": 46},
        {"want": r"uv version --bump {{ INCREMENT }}", "start": 96, "end": 100},
    ]
    for t in cases:
        lines = get_lines(start=t["start"], end=t["end"], content=got)
        assert t["want"] in lines


def test_gitlab_ci_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / ".gitlab-ci.yml").read_text()
    want_1 = f'PYTHON_VERSION: "{PY_VERSION}"'
    want_2 = "--cov=example"
    assert want_1 in got
    assert want_2 in got


def test_license_MIT_renders_correct(session_tmp_path: Path):  # noqa: N802
    got = (session_tmp_path / "LICENSE").read_text()
    want = f"Copyright (c) {CUR_YEAR} John Doe"
    assert want in got


def test_zensical_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / "zensical.toml").read_text()
    cases: list[str] = [
        'site_name = "Example - Documentation"',
        'site_author = "John Doe"',
        'copyright = """\nCopyright &copy; 2025 John Doe\n"""',
        'media = "(prefers-color-scheme)"',
        'media = "(prefers-color-scheme: light)"',
        'media = "(prefers-color-scheme: dark)"',
    ]
    for want in cases:
        assert want in got


def test_test_platform_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / ".github/workflows/test_platform.yml").read_text()
    want_1 = (
        "python-version:\n"
        f'          - "{PY_VERSION_PAST}"\n'
        f'          - "{PY_VERSION}"\n'
        f'          - "{PY_VERSION_FUTURE}"'
    )
    assert want_1 in got


def test_test_coverage_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / ".github/workflows/test_coverage.yml").read_text()
    want_1 = "--cov=example"
    want_2 = "GITHUB_TOKEN: ${{ github.token }}"
    assert want_1 in got
    assert want_2 in got


def test_publish_renders_correct(session_tmp_path: Path):
    got = (session_tmp_path / ".github/workflows/publish.yml").read_text()
    want = f"run: uv python install {PY_VERSION}"
    assert want in got
