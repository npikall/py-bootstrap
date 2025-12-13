_default:
    @just --list

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
