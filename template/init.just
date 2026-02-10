# initialize a git repo and setup venv
init: venv
    git init
    just hooks
    @just _remove_init
    git add .
    git commit -m "initial commit"
    @echo "{{ GREEN }}{{ BOLD }}Git has been initialized{{ NORMAL }}"


_remove_init:
    find . -name 'init.just' -exec rm -f {} +
    sed '5,6d' Justfile > Justfile.tmp && mv Justfile.tmp Justfile
