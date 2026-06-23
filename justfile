set windows-shell := ["powershell"]

# Default command lists all available recipes
[default]
_default:
    @just --list --unsorted

alias c := clean
alias d := docs
alias h := hooks
alias i := info
alias l := lint
alias q := check
alias t := test
alias hi := hooks-install
alias fmt := format

# display the system/project information
info:
    @echo "{{ CYAN }}Arch{{ NORMAL }}: {{ arch() }}"
    @echo "{{ CYAN }}OS{{ NORMAL }}: {{ os_family() }}, {{ os() }}"
    @echo "{{ CYAN }}Num CPU's{{ NORMAL }}: {{ num_cpus() }}"
    @echo "{{ CYAN }}Project{{ NORMAL }}: `uv version`"

# run the linter [arg:<full|concise|...>]
lint arg="concise":
    uv run ruff check . --fix --output-format={{ arg }}

# run the formatter
format:
    uv run ruff format .

# run the type checker [arg:<full|concise|...>]
types arg="concise":
    uv run ty check --output-format={{ arg }}

# lint, format and type-check [arg:<full|concise|...>]
check arg="concise":
    -@just format
    -@just lint {{ arg }}
    -@just types {{ arg }}

# run the tests
test *args:
    uv run pytest tests/ {{ args }}

# run the tests in different Python versions
testall *args:
    uv run --python=3.12 pytest {{ args }}
    uv run --python=3.14 pytest {{ args }}

# run the formatter, linter, typechecker and the tests
ci python="3.13":
    uv run --python={{ python }} ruff format .
    uv run --python={{ python }} ruff check . --fix
    uv run --python={{ python }} ty check .
    uv run --python={{ python }} pytest tests/

# install the pre-commit hooks
hooks-install:
    uvx prek install

# run the pre-commit hooks
hooks:
    uvx prek run --all-files

# setup the workspace
dev: hooks-install venv

# clean all build/compilation and cache files and directories
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
    rm -fr rendered/
    rm -fr site/
    find . -name '*.egg' -exec rm -f {} +
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '.DS_Store' -exec rm -fr {} +
    find . -name '__pycache__' -exec rm -fr {} +

# install dependencies in local venv
venv:
    uv sync --all-groups --all-extras

# serve the documentation on localhost
docs: venv
    uv run zensical serve


# render template to a temp dir for manual inspection
render:
    copier copy . ./rendered --overwrite --trust --defaults -r HEAD \
        --data project_name=example \
        --data author_fullname="John Doe" \
        --data author_email=john.doe@mail.com \
        --data author_username=jdoe \
        --data ci_github=true \
        --data 'ci_github_workflows=["Lint_Format", "Documentation", "Publish_PyPI", "Release_GitHub", "Test_Coverage", "Test_Platforms"]' \
        --data ci_gitlab=true \
        --data repo_name=example \
        --data include_docs=true \
        --data changelog_tool=git-cliff \
        --data copyright_license=MIT

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
changelog *args:
    uvx git-cliff -o {{ args }}

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock CHANGELOG.md
    git commit -m "chore(release): bump version to {{ version }}"
    git tag -a "v{{ version }}"

_update_template_and_commit:
    uvx prek auto-update
    uv run scripts/update_template_dependencies.py
    -just hooks
    git add .
    -git commit -m "chore(template): update template dependencies"

# make a new release [target:<major|minor|patch|...> or semver]
release target: ci
    @just _ensure_clean
    @just _update_template_and_commit
    @just _set_version {{ target }}
    @just changelog --tag `uv version --short`
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
