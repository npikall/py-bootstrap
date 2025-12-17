from pathlib import Path

import pytest
from copier import run_copy
from pydantic import BaseModel, Field


class UserAnswers(BaseModel):
    project_name: str = Field(default="example")
    author_fullname: str = Field(default="John Doe")
    author_email: str = Field(default="john.doe@mail.com")
    author_username: str = Field(default="jdoe")
    ci_github: bool = Field(default=True)
    ci_gitlab: bool = Field(default=True)
    repo_name: str = Field(default="example")
    copyright_license: str = Field(default="MIT")
    include_docs: bool = Field(default=True)


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
    ]

    for file in want:
        assert (session_tmp_path / file).exists()


def test_readme_renders_correct(session_tmp_path):
    want = "# example"
    assert want in (session_tmp_path / "README.md").read_text()
