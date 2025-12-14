---
icon: lucide/layout-template
tags:
  - template
---

# The Template

## Layout

The template generates a package structure that reflects common best practices for Python projects. The layout shown below represents the full set of files and directories that may be created by the template. Depending on the configuration choices you made during setup, some of these files or components may be omitted automatically.

```bash
<PROJECT> ---------------------- # your freshly created project!
├── .copier-answers.yml -------- # Copier Answer to update project
├── .gitignore ----------------- #
├── .gitlab-ci.yml ------------- # Gitlab CI Config
├── .pre-commit-config.yml ----- #
├── .python-version ------------ #
├── CONTRIBUTING.md ------------ #
├── Justfile ------------------- # Taskrunner
├── LICENSE -------------------- #
├── README.md ------------------ #
├── pyproject.toml ------------- # Project Config
├── src/<PROJECT> -------------- # Python Package
│   └── __init__.py ------------ #
├── tests ---------------------- # Tests for the Package
│   └── test_meta.py ----------- #
├── docs ----------------------- # Documentation pages
│   └── index.md --------------- #
├── zensical.toml -------------- #
└── .github -------------------- # Github CI Config
    └── ... -------------------- #
```

## Github CI

The template includes a set of `GitHub Actions` workflows that automate common development and release tasks. These workflows ensure code quality, reliability, and consistency without requiring manual intervention.

Under `.github/workflows`, the configuration is split into focused pipelines:

- linting, formatting and typechecking with `ruff` and `ty`
- running tests with coverage (also produces a coverage badge)
- validating the package across multiple platforms and Python versions
- publishing the documentation to GitHub Pages
- releasing the package to PyPI

Together, these workflows provide a lightweight but complete CI/CD setup that supports the project from development through distribution.

```bash
└── .github -------------------- # Github CI Config
    ├── actions/setup ---------- #
    │   └── setup.yml ---------- #
    └── workflows -------------- #
        ├── code_quality.yml --- # Lint, Format and Typechecking
        ├── docs.yml ----------- # Documentation on Github Pages
        ├── publish.yml -------- # Publish to PyPi
        ├── test_coverage.yml -- # Run tests with coverage
        └── test_platform.yml -- # Test different platforms and versions
```

## Task Orchestration with `Justfile`

The template uses a `Justfile` to provide a simple and consistent interface for task orchestration. It groups common development, quality assurance, and release tasks behind short, memorable commands, reducing the need to remember long tool-specific invocations. Most commands are built on top of uv, ensuring fast and reproducible execution.

Here are some of the core tasks provided:

- `just` Lists all available tasks and aliases.
- `just check` or `just q` Run linting and formatting with ruff and type checking with ty.
- `just test` or `just t` Run the test suite.
- `just testall` Run the test suite against all supported Python versions.
  just ci
- `just ci` Execute formatting, linting, type checks, and tests in a single command, mirroring the CI pipeline locally.
- `just clean` or `just c` Remove build artifacts, caches, and test outputs.
- `just venv` Install and synchronize all project dependencies into the local virtual environment.
- `just hooks` or `just h` Install the pre-commit hooks.
- `just bump <major|minor|patch>` or `just b` Bump the project version with confirmation and create a corresponding Git tag.
- `just dist` or `just d` Build the source distribution and wheel.
- `just docs` Serve the documentation locally.
- `just init` Initialize a Git repository, install dependencies and hooks, and create the initial commit.

## Pre-commit Hooks

The template comes with a curated set of _pre-commit hooks_ that enforce code quality and repository hygiene before changes are committed. These hooks run automatically on each commit, providing fast feedback and preventing common issues from entering the codebase. They are designed to align with the checks performed in CI, ensuring consistency between local development and automated pipelines.

Provided hooks include:

- **Ruff linting and formatting**
  Automatically lint and format Python code using `ruff`, applying fixes where possible to keep the codebase consistent.

- **Dependency lockfile synchronization**
  Ensures the `uv` lockfile is kept up to date whenever dependencies change, preventing drift between configuration and resolved environments.

- **Whitespace and file hygiene checks**
  Prevent common formatting issues such as trailing whitespace and missing end-of-file newlines.

- **Repository safety checks**
  Detects accidentally committed private keys and blocks unusually large files from being added to the repository.

Together, these hooks act as a first line of defense, catching errors early and reducing friction during code review and continuous integration.

Pre-commit hook versions are pinned in `.pre-commit-config.yaml` and should be updated periodically. To upgrade all hooks to their latest compatible versions, run:

=== "`pre-commit`"

    If the `pre-commit` tool is installed.
    ```console
    pre-commit autoupdate
    ```

=== "`uvx`"

    If the `pre-commit` tool is not installed.
    ```console
    uvx pre-commit autoupdate
    ```

## GitLab CI

The template includes a lightweight `GitLab CI` configuration that mirrors the most important quality checks performed locally and in GitHub Actions. It is designed to provide fast feedback while remaining easy to adapt to project-specific requirements.

The pipeline is split into two stages, `test` and `build`, and relies on containerized tools to ensure reproducible execution.

Key components include:

- **Stage-based pipeline**
  A `test` stage for executing the test suite and a `build` stage for static analysis and formatting checks.

- **uv-powered test job**
  A dedicated job runs tests using _uv_ inside an official container image, installing dependencies and executing the test suite with coverage reporting enabled.

- **Reusable Ruff base job**
  A shared base configuration defines the _ruff_ image and setup, reducing duplication across linting and formatting jobs.

- **Ruff linting with GitLab integration**
  The linting job exports results in GitLab’s code quality format, allowing issues to be displayed directly in merge requests.

- **Ruff formatting checks**
  A formatting job verifies that the codebase is properly formatted by running `ruff format` in diff mode.

Overall, this configuration provides a concise yet effective CI setup for GitLab, ensuring code quality and test coverage while keeping the pipeline easy to maintain.

## Licenses

The template allows you to choose between several widely used open-source licenses. Each option provides a different balance between permissiveness, attribution requirements, and legal protection. Selecting an appropriate license early helps set clear expectations for users and contributors of your project.

<!-- TODO: Verify table, as it might be faulty -->

??? note "Choose a License"

    Checkout [ChooseALicense](https://choosealicense.com/licenses/) to find more detailed explanations of the Licenses.

| License        | Permissive | Requires Attribution | Patent Grant | Warranty Disclaimer | Typical Use Case                                                           |
| -------------- | ---------- | -------------------- | ------------ | ------------------- | -------------------------------------------------------------------------- |
| **MIT**        | Yes        | Yes                  | No           | Yes                 | Simple, permissive licensing with minimal requirements                     |
| **Apache 2.0** | Yes        | Yes                  | Yes          | Yes                 | Projects that want explicit patent protection and clear contribution terms |
| **Unlicense**  | Yes        | No                   | No           | Yes                 | Public-domain–like release with no usage restrictions                      |

In short, **MIT** is a lightweight and popular choice, **Apache 2.0** adds explicit patent protections, and **Unlicense** removes nearly all restrictions by dedicating the work to the public domain.

## Copier Answers

The template includes a `.copier-answers.yml` that records the choices you made when generating the project. This file allows the project to be _updateable_: when the template is updated in the future, Copier can reapply the changes to your existing project while preserving your customizations.

By maintaining this answers file, you ensure that updates to the template, such as new workflows, configuration improvements, or additional files, can be integrated safely and consistently without overwriting your work.

## Pyproject

The template includes a `pyproject.toml` configuration file that defines project-wide settings for tools like _ruff_. The linting rules follow a simple philosophy: **enable all rules by default** to maximize code quality, and **disable only those that are non-sensical or conflict with project conventions**.

This approach ensures comprehensive static analysis while minimizing unnecessary noise, helping maintain a clean and consistent codebase.
