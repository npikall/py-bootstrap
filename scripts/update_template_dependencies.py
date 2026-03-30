import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class GitRepoError(Exception):
    """Base Exception for Git Repo Path."""


def main():
    root = get_project_root()
    template_dir = root / "template"
    process_pyproject_dependencies(template_dir)


def process_pyproject_dependencies(template_dir: Path) -> None:
    file = template_dir / "pyproject.toml"
    with file.open("rb") as f:
        data = tomllib.load(f)
    print(PyprojectModel.model_validate(data))
    # raise NotImplementedError


def get_project_root() -> Path:
    current_filepath = Path(__file__)
    root_marker_file = "pyproject.toml"
    for parent in current_filepath.parents:
        if (parent / root_marker_file).exists():
            return parent
    err = f"no '{root_marker_file}' found in any parent directories"
    raise FileNotFoundError(err)


class BuildSystem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    requires: list[str]


class PyprojectModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    build_system: BuildSystem = Field(alias="build-system")


if __name__ == "__main__":
    main()
