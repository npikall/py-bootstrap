---
icon: lucide/refresh-cw
tags:
  - copier
  - update
---

# Update an existing Project

## Updateable Project Foundations

Projects generated with this Copier template are not static snapshots. Instead, they are designed to stay connected to the source template and can be updated at any time. This allows improvements, bug fixes, and new best practices introduced in the template to be applied to existing projects without starting from scratch.

By building updateability into the project from the beginning, the template helps reduce long-term maintenance costs, avoid configuration drift, and keep tooling, workflows, and project structure aligned with current standards as the template evolves.

For more in-depth explanations visit [`copier`](https://copier.readthedocs.io/en/stable/updating/)

## How Template Updates Work

`Copier` keeps track of your original template choices in the `.copier-answers.yml` file. This allows it to reapply changes from the source template onto your existing project while preserving your custom modifications.

!!! info

    `Git` needs to be initalized in the repo, and all changes commited, for the update to work properly.
    The changes can then be viewed and commited if wanted.

To update a project from the template, run the following command in the root of your project:

```bash
copier update
```

Copier will fetch the latest version of the template, compare it against your current project state, and apply any new or changed files. If conflicts arise, Copier will prompt you to resolve them interactively, similar to a Git merge.

If you want to update from a specific template revision, you can pin the update explicitly:

```bash
copier update --vcs-ref <tag-or-commit>
```

This workflow makes it possible to continuously adopt template improvements in a controlled and transparent manner, without losing project-specific changes.
