# ruff: noqa: D100, D101, D103 INP001
import shutil
from datetime import date
from enum import StrEnum, auto
from pathlib import Path

import httpx
from packaging.version import parse
from pydantic import BaseModel, ConfigDict, TypeAdapter
from rich import print  # noqa: A004

PROJECT_DIRECTORY = Path.cwd().resolve()


class EndOfLifeResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    cycle: str
    releaseDate: date  # noqa: N815
    eol: date


eol_list_adapter = TypeAdapter(list[EndOfLifeResponse])


def _request_python_versions() -> list[EndOfLifeResponse]:
    url = "https://endoflife.date/api/python.json"
    resp = httpx.get(url)
    resp.raise_for_status()
    data = resp.json()
    return eol_list_adapter.validate_python(data)


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


def update_python() -> None:
    """Update Python versions in Template.

    To be run manually.
    """
    m: list[EndOfLifeResponse] = _request_python_versions()
    m.sort(key=lambda x: parse(x.cycle), reverse=True)
    future_version = m[0].cycle
    current_version = m[1].cycle
    previous_versions_1 = m[2].cycle
    previous_versions_2 = m[3].cycle
    previous_versions_3 = m[4].cycle

    re_mapping: dict[str, str] = {
        "[PY_VERSION_F]": future_version,
        "[PY_VERSION_C]": current_version,
        "[PY_VERSION_1]": previous_versions_1,
        "[PY_VERSION_2]": previous_versions_2,
        "[PY_VERSION_3]": previous_versions_3,
    }

    files_to_update: list[str] = [
        "Justfile",
        ".python-version",
        "pyproject.toml",
        ".gitlab-ci.yml",
        ".github/workflows/run_tests.yml",
    ]

    for file in files_to_update:
        filepath = PROJECT_DIRECTORY / file
        old_contents = filepath.read_text()
        new_contents = old_contents

        for old, new in re_mapping.items():
            new_contents = new_contents.replace(old, new)

        with filepath.open("w", encoding="utf-8") as f:
            f.write(new_contents)
        print(f"Updated: {filepath}")


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

    update_python()

    print(":rocket: [green bold] Project successfully initialized.")


if __name__ == "__main__":
    main()
