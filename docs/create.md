---
icon: lucide/file-plus
tags:
  - create
  - new
---

# Creating a new project

## Commandline

To create a new project from this template run the following command:

```console
copier copy --trust "gh:npikall/py-bootstrap" path/to/project/
```

If you don't have `copier` installed, you can also use the [`uv`][uv] tool runner:

```console
uvx --with copier-templates-extensions copier copy --trust "gh:npikall/py-bootstrap" /path/to/new/project
```

## Prompt

The Template will ask you a bunch of questions, and configures the templates, to your input.

These Questions will look something like this:

```console
-> Set the project name:
   example-project
```

```console
-> Set the project's license:
   - MIT
   - Apache 2.0
   - The Unlicense
```

```console
-> Include Docs from Zensical
   (Y/n)
```

[uv]: https://docs.astral.sh/uv/
