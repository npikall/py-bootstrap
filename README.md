# Cookiecutter `Py-Lib`

This template sets up a structure for you to write a python package.
It comes filled with a bunch of modern features from the python ecosystem.

## :battery: All Batteries included

- :wrench: CI pipelines for `Github Actions` and `Gitlab`
- :scroll: Documentation from [Zensical] (the followup project to [Material for MKDocs])
- :zap: Fast environment and project management with [uv]
- :musical_note: Task orchestration with [Just]
- :black_nib: Preconfigured Licenses to choose from
- :straight_ruler: Testing setup with `pytest`
- :fishing_pole_and_fish: Pre-commit Hooks
- :mag: Code Quality assurance with [ruff] and [ty]

## Useage

To install the `copier` tool with [uv] run:

```console
uv tool install copier --with copier-templates-extensions
```

To initialize a new repository with the `copier` template run the following command:

```console
copier copy --trust "gh:npikall/cookiecutter-py-lib" path/to/project/
```

You will be prompted and then your repo will be setup.

[Just]: https://github.com/casey/just
[Zensical]: https://zensical.org/
[Material for MKDocs]: https://squidfunk.github.io/mkdocs-material/
[uv]: https://docs.astral.sh/uv/
[ruff]: https://docs.astral.sh/ruff/
[ty]: https://docs.astral.sh/ty/
