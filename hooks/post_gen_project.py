# ruff: noqa: D100, D101, D103, EXE001
import shutil
from enum import StrEnum, auto
from pathlib import Path

from rich import print

PROJECT_DIRECTORY = Path.cwd().resolve()


class SupportedCI(StrEnum):
    GITHUB = auto()
    GITLAB = auto()
    ALL = auto()


class PromptBool(StrEnum):
    YES = auto()
    NO = auto()


def remove_file(file: str) -> None:
    filepath: Path = PROJECT_DIRECTORY / file
    filepath.unlink()


def remove_dir(directory: str) -> None:
    dir_path: Path = PROJECT_DIRECTORY / directory
    shutil.rmtree(dir_path)


def main() -> None:
    # Prompted variable values
    ci_framwork: SupportedCI = "{{ cookiecutter.ci_framework }}"  # type: ignore[invalid-asignment]
    has_ci_code_quality: PromptBool = "{{ cookiecutter.ci_code_quality_check }}"  # type: ignore[invalid-asignment]
    include_docs: PromptBool = "{{ cookiecutter.include_docs }}"  # type: ignore[invalid-asignment]

    if include_docs == PromptBool.NO:
        remove_file("zensical.toml")
        remove_dir("docs")

    match ci_framwork:
        case SupportedCI.GITLAB:
            # Remove everything but Gitlab
            remove_dir(".github")
        case SupportedCI.GITHUB:
            # Remove everything but Github
            remove_file(".gitlab-ci.yml")
        case SupportedCI.ALL:
            # Delete none
            pass
        case _:
            err = f"""
            The repository {ci_framwork!r} specified in cookiecutter.ci_framwork,
            is currently not supported.
            Must be one of {[member.value for member in SupportedCI]}.
            """
            raise NotImplementedError(err)

    if has_ci_code_quality == PromptBool.NO:
        remove_file(".github/workflows/code_quality.yml")
        remove_file(".github/actions/setup/action.yml")
    print(":rocket: [green bold] Project successfully initialized.")


if __name__ == "__main__":
    main()
