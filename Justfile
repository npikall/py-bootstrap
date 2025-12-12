_default:
    @just --list

# setup the python virtual environment (with uv)
setup:
    uv sync

# update dependencies
update:
    cd template && uvx pre-commit autoupdate
