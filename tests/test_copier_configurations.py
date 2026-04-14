from pathlib import Path

import pytest
from conftest import DefaultUserAnswer
from copier import run_copy

CWD = Path(__file__).resolve().parent.parent


def setup_test(
    given: DefaultUserAnswer, path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_copy(
        src_path=str(CWD),
        dst_path=path,
        unsafe=True,
        data=given.model_dump(),
        vcs_ref="HEAD",
    )
    _ = capsys.readouterr()


def test_pyproject_toml_excludes_git_cliff_config_when_git_changelog_selected(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(changelog_tool="git-changelog")
    setup_test(given, tmp_path, capsys)
    pyproject_content = (tmp_path / "pyproject.toml").read_text()
    assert "git-cliff" not in pyproject_content


def test_pyproject_toml_excludes_docs_dependencies_when_no_docs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(include_docs=False)
    setup_test(given, tmp_path, capsys)
    pyproject_content = (tmp_path / "pyproject.toml").read_text()
    assert "mkdocstrings-python" not in pyproject_content
    assert "zensical" not in pyproject_content


def test_pyproject_toml_uses_custom_py_dist_name(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(
        py_dist_name="my-custom-package",
        py_import_name="my_custom_module",
    )
    setup_test(given, tmp_path, capsys)
    pyproject_content = (tmp_path / "pyproject.toml").read_text()
    assert "--cov=my-custom-package" in pyproject_content


def test_package_structure_uses_custom_py_import_name(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(
        py_dist_name="my-custom-package",
        py_import_name="my_custom_module",
    )
    setup_test(given, tmp_path, capsys)
    custom_module_dir = tmp_path / "src" / "my_custom_module"
    assert custom_module_dir.exists()

    init_file = custom_module_dir / "__init__.py"
    assert init_file.exists()

    test_meta_file = tmp_path / "tests" / "test_meta.py"
    test_content = test_meta_file.read_text()
    assert "from my_custom_module import greet" in test_content


def test_greeting_function_uses_custom_py_dist_name(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(
        py_dist_name="my-custom-package",
        py_import_name="my_custom_module",
    )
    setup_test(given, tmp_path, capsys)
    init_file = tmp_path / "src" / "my_custom_module" / "__init__.py"
    init_content = init_file.read_text()
    assert '"Hello from my-custom-package"' in init_content


def test_justfile_excludes_docs_commands_when_no_docs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(include_docs=False)
    setup_test(given, tmp_path, capsys)
    justfile = tmp_path / "Justfile"
    just_content = justfile.read_text()
    assert "alias d := docs" not in just_content
    assert "docs: venv" not in just_content
    assert "uv run zensical serve" not in just_content


def test_justfile_includes_git_changelog_changelog_command(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(changelog_tool="git-changelog")
    setup_test(given, tmp_path, capsys)
    justfile = tmp_path / "Justfile"
    just_content = justfile.read_text()
    assert "uvx git-cliff" not in just_content
    assert "uvx git-changelog" in just_content


def test_zensical_uses_project_name_from_config(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(project_name="my-awesome-project")
    setup_test(given, tmp_path, capsys)
    zensical = tmp_path / "zensical.toml"
    zensical_content = zensical.read_text()
    assert "My-awesome-project" in zensical_content


def test_contributing_uses_correct_repo_link(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(repo_name="awesome-repo")
    setup_test(given, tmp_path, capsys)
    contributing = tmp_path / "CONTRIBUTING.md"
    contributing_content = contributing.read_text()
    assert "github.com/jdoe/awesome-repo" in contributing_content


def test_readme_uses_project_name_from_config(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
):
    given = DefaultUserAnswer(project_name="my-unique-project")
    setup_test(given, tmp_path, capsys)
    readme = tmp_path / "README.md"
    readme_content = readme.read_text()
    assert "# my-unique-project" in readme_content


def test_copier_answers_file_is_created(copied_project: Path):
    copier_answers_files = list(copied_project.glob(".copier-answers.yml"))
    assert len(copier_answers_files) == 1
    answers_content = copier_answers_files[0].read_text()
    assert "project_name:" in answers_content
    assert "author_fullname:" in answers_content
