---
icon: lucide/hammer
tags:
  - setup
---

# Setup

## Prerequistes

In order to have no issues useing this Template make sure the following software is installed.

- [`Git v2`](https://git-scm.com), a version control system
- [`Python 3`][Python], which can be managed with [uv]
- [`Copier`][Copier], the Python Program that creates the templates
- [`uv`][uv], a Python Package Manager (optional)
- [`just`][just], the Taskrunner used inside the template (recommended)

## Install Python

Install [`uv`][uv] with the following command.

```console
curl -LsSf https://astral.sh/uv/install.sh | sh
```

And install [`Python`][Python] with [`uv`][uv] by running

```console
uv python install 3.12
```

## Install Copier

Run the following commands to install [`Copier`][Copier] as a `CLI` Tool.

=== "`uv`"

    ```console
    uv tool install copier --with copier-templates-extensions
    ```

=== "`pipx`"

    ```console
    pipx install copier
    pipx inject copier copier-templates-extensions
    ```

[Python]: https://www.python.org
[uv]: https://docs.astral.sh/uv/
[Copier]: https://copier.readthedocs.io/en/stable/
[just]: https://github.com/casey/just
