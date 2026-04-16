set windows-shell := ["powershell"]

# Default command lists all available recipes
[default]
_default:
    @just --list

alias c := clean
alias d := docs
alias h := hooks
alias i := info
alias l := lint
alias q := check
alias t := test
alias hi := hooks-install
alias ua := update-all
alias fmt := format

# display the system/project information
[group("chore")]
info:
    @echo "{{ CYAN }}Arch{{ NORMAL }}: {{ arch() }}"
    @echo "{{ CYAN }}OS{{ NORMAL }}: {{ os_family() }}, {{ os() }}"
    @echo "{{ CYAN }}Num CPU's{{ NORMAL }}: {{ num_cpus() }}"
    @echo "{{ CYAN }}Project{{ NORMAL }}: `uv version`"

# run the linter [arg:<full|concise|...>]
[group("style")]
lint arg="concise":
    uv run ruff check . --fix --output-format={{ arg }}

# run the formatter
[group("style")]
format:
    uv run ruff format .

# run the type checker [arg:<full|concise|...>]
[group("style")]
types arg="concise":
    uv run ty check --output-format={{ arg }}

# lint, format and type-check [arg:<full|concise|...>]
[group("style")]
check arg="concise":
    -@just lint {{ arg }}
    -@just format
    -@just types {{ arg }}

# run the tests
[group("test")]
test *args:
    uv run pytest tests/ {{ args }}

# run the tests in different Python versions
[group("test")]
testall *args:
    uv run --python=3.12 pytest {{ args }}
    uv run --python=3.14 pytest {{ args }}

# run the formatter, linter, typechecker and the tests
[group("test")]
ci python="3.13":
    uv run --python={{ python }} ruff format .
    uv run --python={{ python }} ruff check . --fix
    uv run --python={{ python }} ty check .
    uv run --python={{ python }} pytest tests/

# install the pre-commit hooks
[group("dev")]
hooks-install:
    uvx prek install

# run the pre-commit hooks
[group("dev")]
hooks:
    uvx prek run --all-files

# setup the workspace
[group("dev")]
dev: hooks-install venv

# clean all build/compilation and cache files and directories
[group("dev")]
clean:
    rm -fr .cache/
    rm -fr .coverage
    rm -fr .eggs/
    rm -fr .pytest_cache/
    rm -fr .ruff_cache/
    rm -fr .venv/
    rm -fr build/
    rm -fr dist/
    rm -fr htmlcov/
    rm -fr init.just
    rm -fr site/
    find . -name '*.egg' -exec rm -f {} +
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '.DS_Store' -exec rm -fr {} +
    find . -name '__pycache__' -exec rm -fr {} +

# install dependencies in local venv
[group("dev")]
venv:
    uv sync --all-groups --all-extras

# update dependencies in the lock file
[group("dev")]
update:
    uv lock --upgrade
    uvx prek auto-update

# update all dependencies in the repo and the template
[group("dev")]
update-all:
    uv lock --upgrade
    uvx prek auto-update
    uv run scripts/update_template_dependencies.py

# build the source distribution and wheel file
[group("dev")]
dist:
    uv build

# serve the documentation on localhost
[group("dev")]
docs: venv
    uv run zensical serve

_ensure_clean:
    @git diff --quiet
    @git diff --cached --quiet

_set_version target:
    case "{{ target }}" in \
        [0-9]*.[0-9]*.[0-9]*) \
            uv version {{ target }} ;; \
        *) \
            uv version --bump {{ target }} ;; \
    esac
    uv lock

# write the changelog from commit messages (https://git-cliff.org/)
[group("chore")]
changelog *args:
    uvx git-cliff -o {{ args }}

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock CHANGELOG.md
    git commit -m "chore(release): bump version to {{ version }}"
    git tag -a "v{{ version }}"

_update_template_and_commit:
    uv run scripts/update_template_dependencies.py
    git add .
    git commit -m "chore(template): update template dependencies"

# make a new release [target:<major|minor|patch|...> or semver]
[group("chore")]
release target: ci
    @just _ensure_clean
    @just _update_template_and_commit
    @just _set_version {{ target }}
    @just changelog --tag `uv version --short`
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
