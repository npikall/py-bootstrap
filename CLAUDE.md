# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyBootstrap is a **copier template** for bootstrapping new Python packages with modern tooling. When users run `copier copy`, this template generates a new Python project structure based on their answers to prompts defined in `copier.yml`.

## Development Commands

```bash
# Install dependencies and create virtual environment
just setup

# Run all tests
just test

# Run CI pipeline (format, lint, typecheck, tests)
just ci

# Serve documentation locally
just docs

# Clean build artifacts
just clean

# Create a release (target can be "major", "minor", "patch", or a semver version)
just release <target>
```

## Architecture

### Template Structure

The core template files live in the `template/` directory. These are Jinja2 templates (suffixed with `.jinja`) that get rendered when users run copier:

- `copier.yml` - Defines user prompts (project_name, author, license choices, etc.)
- `extensions.py` - Custom Jinja2 extensions for template rendering:
  - `GitExtension` - Filters for `git_user_name()` and `git_user_email()`
  - `SlugifyExtension` - `slugify()` filter for converting strings to URL-safe names
  - `CurrentYearExtension` - `current_year` global variable
- `template/` - Contains all files that will be copied into the generated project

### Conditional Rendering

Template files can be conditionally included based on user choices using Jinja2 conditionals in filenames:

```
{% if ci_github %}.github{% endif %}
{% if include_docs and docs_engine == "mkdocs" %}mkdocs.yml{% endif %}
{% if copyright_license != "None" %}LICENSE{% endif %}
```

Key user choices affecting output:
- `ci_github` / `ci_gitlab` - Which CI pipelines to include
- `include_docs` / `docs_engine` - Documentation (zensical or mkdocs)
- `copyright_license` - MIT, Apache-2.0, Unlicense, or None

### Key Derived Variables

`copier.yml` defines computed values (marked `when: false`) that are derived from user input:
- `py_dist_name` - Package name for pip install (e.g., "my-package")
- `py_import_name` - Python import name (e.g., "my_package")
- `copyright_date` - Current year
- `copyright_holder` - Author's full name
- `py_version_*` - Past (3.10), current (3.12), future (3.14) Python versions

### Testing

Tests validate that the template renders correctly using `copier.run_copy()`:

```python
from copier import run_copy

run_copy(
    src_path=str(cwd),
    dst_path=session_tmp_path,
    unsafe=True,
    data=user_answers.model_dump(),
    vcs_ref="HEAD",
)
```

- `tests/conftest.py` - Defines test fixtures: `FullUserAnswers` and `BaseUserAnswers` with default values
- `tests/test_copier.py` - Validates generated files contain expected content
- `tests/test_licenses.py` - Tests license rendering
- `tests/test_jinja_tags.py` - Tests custom Jinja2 extensions
- `tests/test_docs.py` - Tests documentation rendering

## Tooling

- **uv** - Python package and environment manager
- **Just** - Task runner for `just` commands
- **ruff** - Linter and formatter
- **ty** - Type checker
- **pytest** - Test framework
- **copier** - Template engine
- **zensical** - Documentation generator
- **prek** - Pre-commit hook manager (alternative to pre-commit)

## Code Quality

- Pre-commit hooks run ruff formatter, ruff linter, and pyproject-fmt
- CI runs on every push to validate lockfile, linting, formatting, type checking, and tests
- Ruff is configured with `line-length = 88` and `lint.select = ["ALL"]` with specific ignores