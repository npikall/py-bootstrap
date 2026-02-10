[default]
_default:
    @just --list

alias t := test
alias d := docs

# display the system/project information
[group("chore")]
info:
    @echo "{{ CYAN }}Arch{{ NORMAL }}: {{ arch() }}"
    @echo "{{ CYAN }}OS{{ NORMAL }}: {{ os_family() }}, {{ os() }}"
    @echo "{{ CYAN }}Num CPU's{{ NORMAL }}: {{ num_cpus() }}"
    @echo "{{ CYAN }}Project{{ NORMAL }}: `uv version`"

# setup the python virtual environment (with uv)
[group("dev")]
setup:
    uv sync --all-groups

# update pre-commit hooks
[group("dev")]
update:
    uvx prek autoupdate
    uv lock --upgrade

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
    find . -name '.cache' -exec rm -fr {} +
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

# write the changelog (using "github.com/pawamoy/git-changelog")
[group("chore")]
changelog version=`uv version --short`:
    uvx git-changelog -Tio CHANGELOG.md -B="{{ version }}" -c conventional

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock CHANGELOG.md
    git commit -m "chore(release): bumped version to {{ version }}"
    git tag -a "v{{ version }}"

# make a new release (target can be <major,minor,patch,...> or semver)
[group("chore")]
release target: test
    @just _ensure_clean
    @just _set_version {{ target }}
    @just changelog "v`uv version --short`"
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"
