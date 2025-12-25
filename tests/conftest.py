from pydantic import BaseModel


class BaseUserAnswers(BaseModel):
    project_name: str = "example"
    author_fullname: str = "John Doe"
    author_email: str = "john.doe@mail.com"
    author_username: str = "jdoe"
    ci_github: bool = True
    ci_gitlab: bool = True
    repo_name: str = "example"
    include_docs: bool = True
    docs_generator: str = "zensical"
    pre_commit: str = "prek"
    use_goreleaser: bool = True


class FullUserAnswers(BaseUserAnswers):
    copyright_license: str = "MIT"


class ChooseLicense(BaseUserAnswers):
    copyright_license: str
