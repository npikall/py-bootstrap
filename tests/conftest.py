import contextlib
import io
from pathlib import Path
from typing import Final, Literal

import pytest
from copier import run_copy
from pydantic import BaseModel

type CopyrightLicenseOptions = Literal["Apache-2.0", "MIT", "Unlicense", "None"]
type ChangelogToolOptions = Literal["git-cliff", "git-changelog"]


DEFAULT_CI_GITHUB_WORKFLOWS: Final = (
    ' ["Lint_Format",'
    ' "Documentation",'
    ' "Publish_PyPI",'
    ' "Release_GitHub",'
    ' "Test_Coverage",'
    ' "Test_Platforms"]'
)

SINGLE_CI_GITHUB_WORKFLOW: Final = ' ["Test_Coverage"]'
DEFAULT_EDITOR_OPTIONS: Final = ' ["editorconfig", "vscode"]'


class DefaultUserAnswer(BaseModel):
    project_name: str = "example"
    author_fullname: str = "John Doe"
    author_email: str = "john.doe@mail.com"
    author_username: str = "jdoe"
    ci_github: bool = True
    ci_github_workflows: str = DEFAULT_CI_GITHUB_WORKFLOWS
    ci_gitlab: bool = True
    repo_name: str = "example"
    include_docs: bool = True
    changelog_tool: ChangelogToolOptions = "git-cliff"
    copyright_license: CopyrightLicenseOptions = "MIT"
    py_dist_name: str = "example"
    py_import_name: str = "example"
    editor: str = DEFAULT_EDITOR_OPTIONS


@pytest.fixture(scope="module")
def copied_project(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_path = tmp_path_factory.mktemp("default")
    cwd = Path(__file__).resolve().parent.parent
    with contextlib.redirect_stdout(io.StringIO()):
        run_copy(
            src_path=str(cwd),
            dst_path=tmp_path,
            unsafe=True,
            data=DefaultUserAnswer().model_dump(),
            vcs_ref="HEAD",
        )
    return tmp_path
