_default:
    @just --list

alias t := test
alias d := docs

# setup the python virtual environment (with uv)
[group("dev")]
setup:
    uv sync --all-groups

# update dependencies
[group("dev")]
update:
    cd template && uvx prek autoupdate

# serve the documentation
[group("dev")]
docs:
    uv sync --group dev
    uv run zensical serve

# run the tests
[group("test")]
test:
    uv run pytest tests/ -rsx --verbose --color=yes

# remove build artifacts
[group("chore")]
clean:
    rm -fr build/
    rm -fr site/
    rm -fr dist/
    rm -fr .eggs/
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -f {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +
    rm -f .coverage
    rm -fr htmlcov/
    rm -fr .pytest_cache

# run all the formatting, linting, and testing commands
[group("test")]
ci:
    uv run ruff format .
    uv run ruff check . --fix
    uv run ty check .
    uv run pytest tests/

# write the changelog
[group("chore")]
changelog VERSION="auto":
    uvx git-changelog -Tio CHANGELOG.md -B="{{VERSION}}" -c angular


# bump the version, commit the changes and add a tag (increment can be major, minor, patch,...)
[group("chore")]
bump VERSION: && tag
    uv version  {{ VERSION }}
    uv lock

# tag the latest version
[group("chore")]
tag VERSION=`uv version --short`:
    git add pyproject.toml
    git add uv.lock
    git commit -m "chore: bumped version to {{VERSION}}"
    git tag -a "v{{VERSION}}"

# make a new release (e.g. "just release 0.1.2") (after all changes have been commited)
[group("chore")]
release VERSION: test
    @just changelog "v{{VERSION}}"
    git add CHANGELOG.md
    git commit -m "chore: updated Changelog"
    @just bump "{{VERSION}}"
    @echo "{{GREEN}}Success! Run 'git push && git push --tags' now.{{NORMAL}}"
