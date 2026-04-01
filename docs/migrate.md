---
icon: lucide/move-up-right
tags:
  - "#migration"
---

# Migrating Old Projects

The `copier` tool allows us to easily transform an old repository, that has not
been created with the template, to one that is linked to a _copier template_.

This can be simply done by just copying the template onto an existing repository.

```bash
# Migrate an old repository to use the template
$ copier copy --trust "gh:npikall/py-bootstrap" path/to/old/repo/
```

If a file from the template is not yet present in the repo `copier` will render
and add it.

If a file already exists `copier` asks the user, wheter or not the file should
be overwritten.
