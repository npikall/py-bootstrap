# Cookiecutter `Py-Lib`

> [!WARNING]  
> This cookiecutter has been deprecated in favor of `copier`

This template or cookiecutter sets up a structure for you to write a python package.
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

To initialize a new repository with this `cookiecutter` template run the following command:

```bash
# if you have cookiecutter installed
cookiecutter https://github.com/npikall/py-bootstrap.git -c cookiecutter

# or if you are using uv
uvx cookiecutter https://github.com/npikall/py-bootstrap.git -c cookiecutter
```

You will be prompted and then your repo will be setup.

[Just]: https://github.com/casey/just
[Zensical]: https://zensical.org/
[Material for MKDocs]: https://squidfunk.github.io/mkdocs-material/
[uv]: https://docs.astral.sh/uv/
[ruff]: https://docs.astral.sh/ruff/
[ty]: https://docs.astral.sh/ty/
