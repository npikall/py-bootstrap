_default:
    @just --list

alias t := test
alias d := docs

# setup the python virtual environment (with uv)
setup:
    uv sync --all-groups

# update dependencies
update:
    cd template && uvx pre-commit autoupdate

# serve the documentation
docs:
    uv sync --group dev
    uv run zensical serve

# run the tests
test:
    uv run pytest tests/ -rsx --verbose --color=yes

# remove build artifacts
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
