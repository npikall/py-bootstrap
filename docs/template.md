---
icon: lucide/layout-template
---

# The Template

!!! warning

    This Site us under Construction :lucide-construction:

## Layout

```console
<PROJECT> ---------------------- # your freshly created project!
├── .copier-answers.yml -------- # Copier Answer to update project
├── .gitignore ----------------- #
├── .gitlab-ci.yml ------------- # Gitlab CI Config
├── .pre-commit-config.yml ----- #
├── .python-version ------------ #
├── CONTRIBUTING.md ------------ #
├── Justfile ------------------- # Taskrunner
├── LICENSE -------------------- #
├── README.md ------------------ #
├── pyproject.toml ------------- # Project Config
├── src/<PROJECT> -------------- # Python Package
│   └── __init__.py ------------ #
├── tests ---------------------- # Tests for the Package
│   └── test_meta.py ----------- #
├── docs ----------------------- # Documentation pages
│   └── index.md --------------- #
├── zensical.toml -------------- #
└── .github -------------------- # Github CI Config
    └── ... -------------------- #
```

## Github CI

```console
└── .github -------------------- # Github CI Config
    ├── actions/setup ---------- #
    │   └── setup.yml ---------- #
    └── workflows -------------- #
        ├── code_quality.yml --- # Lint, Format and Typechecking
        ├── docs.yml ----------- # Documentation on Github Pages
        ├── publish.yml -------- # Publish to PyPi
        ├── test_coverage.yml -- # Run tests with coverage
        └── test_platform.yml -- # Test different platforms and versions
```
