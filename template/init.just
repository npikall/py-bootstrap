# initialize a git repo and setup venv
init: venv
    git init
    just hooks
    find . -name 'init.just' -exec rm -f {} +
    sed -i '5,6d' Justfile
    git add .
    git commit -m "initial commit"
    @echo "{{ GREEN }}{{ BOLD }}Git has been initialized{{ NORMAL }}"
