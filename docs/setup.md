---
icon: lucide/hammer
tags:
  - "#setup"
---

# Setup

## Prerequisites

In order to have no issues using this Template make sure the following software is installed.

- [ ] [`Git v2`](https://git-scm.com), a version control system
- [ ] [`Python 3`][Python], which can be managed with [uv]
- [ ] [`Copier`][Copier], the Python Program that creates the templates
- [ ] [`uv`][uv], a Python Package Manager (optional)
- [ ] [`just`][just], the Taskrunner used inside the template (recommended)

## Install Python

Install [`uv`][uv] with the following command.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

And install [`Python`][Python] with [`uv`][uv] by running

```bash
uv python install 3.12
```

!!! note

    This template supports Testing in Github Actions for Python 3.10, 3.12, and 3.14 (assuming the versions inbetween will work aswell).
    You can install multiple versions if needed:

    ```bash
    uv python install 3.10 3.12 3.14
    ```

## Install Copier

Run the following commands to install [`Copier`][Copier] as a `CLI` Tool.

=== "`uv`"

    ```bash
    uv tool install copier --with copier-templates-extensions
    ```

=== "`pipx`"

    ```bash
    pipx install copier
    pipx inject copier copier-templates-extensions
    ```

## Install Just

[`uv`][uv] has a nice interface to install tools. One of them is [just]. In order to install the [just] binary you can run

```bash
# Install just
uv tool install rust-just
```

Now you can invoke [just] Recipes by calling

```bash
# List all available recipes
$ just
Available Recipes:
    build  # build the package
    docs   # serve the dosumentation

# Execute a recipe
$ just docs
serving docs at https://localhost:8000
```

[Python]: https://www.python.org
[uv]: https://docs.astral.sh/uv/
[Copier]: https://copier.readthedocs.io/en/stable/
[just]: https://github.com/casey/just
