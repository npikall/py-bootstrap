from typing import Literal

from pydantic import BaseModel

type CopyrightLicenseOptions = Literal["Apache-2.0", "MIT", "Unlicense", "None"]
type DocsEngineOptions = Literal["zensical", "mkdocs"]
type PreCommitOptions = Literal["pre-commit", "prek"]
type ChangelogToolOptions = Literal["git-cliff", "git-changelog"]


DEFAULT_CI_GITHUB_WORKFLOWS = (
    ' ["Lint_Format",'
    ' "Documentation",'
    ' "Publish_PyPI",'
    ' "Release_GitHub",'
    ' "Test_Coverage",'
    ' "Test_Platforms"]'
)


class BaseUserAnswers(BaseModel):
    project_name: str = "example"
    author_fullname: str = "John Doe"
    author_email: str = "john.doe@mail.com"
    author_username: str = "jdoe"
    ci_github: bool = True
    ci_github_workflows: str = DEFAULT_CI_GITHUB_WORKFLOWS
    ci_gitlab: bool = True
    repo_name: str = "example"
    include_docs: bool = True
    pre_commit: PreCommitOptions = "prek"
    changelog_tool: ChangelogToolOptions = "git-cliff"


class FullUserAnswers(BaseUserAnswers):
    copyright_license: CopyrightLicenseOptions = "MIT"


class ChooseLicense(BaseUserAnswers):
    copyright_license: CopyrightLicenseOptions
