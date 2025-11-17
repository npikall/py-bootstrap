# {{ cookiecutter.project_slug }}

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

TODO: Add documentation!

> [!IMPORTANT]
> This project uses `uv` for package management and `Just` for task automation.
> To install `uv` check the [uv Docs].
> To install `Just`, follow the instructions in the [Just Docs].

> [!NOTE]
> This cookiecutter tries to adhere to the [Python Developer Tooling Handbook](https://pydevtools.com/handbook/explanation/modern-python-project-setup-guide-for-ai-assistants/)

## First Steps

After you have just used the `cookiecutter` to create this repo, you might want to follow these steps:

1. Initialize a git repo with `git init` or `just init`
2. Install the Pre-Commit Hooks, to identify simple issues before commiting. You can run `just hooks` or use `uvx pre-commit install`
3. Set up a virtual environment. You might want to use `uv add <package>` to add dependencies to your project (no `pip install` necessary)

## Development

The Pre-commit Hooks will lint and format your code, aswell as running some checks.
In order to use the Pre-commit hooks, run:

```bash
uvx pre-commit install
```

or use the Justfile to do the same:

```bash
just hooks
```

By default cody quality checks (formatter, linter and type-checker) are inplace, via `Github Actions` and `GitLab CI/CD`,
which does the same as the `pre-commit` hooks.

Additionally the same code quality checks can be run manually via:

```bash
just check

# or manually with
uvx ruff check . --fix
uvx ruff format .
uvx ty check
```

> [!IMPORTANT]
> The configuration for the linter, the formatter and the typechecker can be done in the `pyproject.toml` file.
> By default ALL Linting Rules are enabled. If some rule are not desired in the project use the `exclude` field to disregard them.

Further more there are example `docs` in this repository, which you can use as a startingpoint for your code documentation.
A certain framework has been choosen, but it only serves as a suggestion to you.

[Just Docs]: https://github.com/casey/just
[uv Docs]: https://docs.astral.sh/uv/getting-started/installation/
