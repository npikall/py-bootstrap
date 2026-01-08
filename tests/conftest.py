from typing import Literal

from pydantic import BaseModel

type CopyrightLicenseOptions = Literal["Apache-2.0", "MIT", "Unlicense", "None"]
type DocsEngineOptions = Literal["zensical", "mkdocs"]
type PreCommitOptions = Literal["pre-commit", "prek"]


class BaseUserAnswers(BaseModel):
    project_name: str = "example"
    author_fullname: str = "John Doe"
    author_email: str = "john.doe@mail.com"
    author_username: str = "jdoe"
    ci_github: bool = True
    ci_gitlab: bool = True
    repo_name: str = "example"
    include_docs: bool = True
    docs_engine: DocsEngineOptions = "zensical"
    pre_commit: PreCommitOptions = "prek"
    use_goreleaser: bool = True


class FullUserAnswers(BaseUserAnswers):
    copyright_license: CopyrightLicenseOptions = "MIT"


class ChooseLicense(BaseUserAnswers):
    copyright_license: CopyrightLicenseOptions
