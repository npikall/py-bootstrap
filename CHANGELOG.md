# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.7] - 2026-03-12

### 🚀 Features

- add pyproject-fmt config
- *(template)* trigger publish to pypi only on created release
- *(template)* conditionally use the chosen changelog tool
- *(template)* prompt for a changelog tool
- *(template)* add git-cliff config if it gets chosen
- *(template)* changelog recipe with two possible bodys
- add git-cliff config

### 🐛 Bug Fixes

- rendering of justfile
- rendering of pyproject toml
- use elif correctly in workflow
- rendering of whitespaces in justfile
- remove pytest ini-options

### 📚 Documentation

- show toc on changelog page

### 🚜 Refactor

- remove boilerplate from readme
- use underscores to render scopes with git-cliff

### 🧪 Testing

- add changelog-tool to the user answers
- update test cases for rendering opitional changelog
- rendering of release recipe
- use underscores instead of stars

### 💼 Other

- use latest justfile from template
- use git-cliff for release note generation
- set fetch-depth to 0 in actions/checkout

## [0.2.6] - 2026-03-10

### 🐛 Bug Fixes

- rendering of args in test recipe correctly
- disallow whitespace characters in pyproject name

### 🚜 Refactor

- replace current year extensions with jinja function

### 🧪 Testing

- copie args in test recipes correctly

### 💼 Other

- *(release)* bumped version to 0.2.6

## [0.2.5] - 2026-03-09

### 🚀 Features

- ci recipe uses current python version

### 🐛 Bug Fixes

- linenumbers to delete in justfile

### 🧪 Testing

- self-destructive init recipe
- read python versions from copier.yml
- ci recipe has dynamic python version

### ◀️ Revert

- remove claude file as no ai is used in the repo
- remove dependabot as its job is redundant

### 💼 Other

- actually use args in justfile recipe
- update python version in ci recipe
- update dependencies
- *(release)* bumped version to 0.2.5

## [0.2.4] - 2026-03-08

### 🚀 Features

- set powershell in justfile for windows users
- update pre-commit hooks
- update build backend version

### 📚 Documentation

- add vhs tape to the readme
- move casette into docs directory

### 🧪 Testing

- iterate over temp dir recursively to find all files

### 💼 Other

- fix documentation recipe
- update pre-commit hooks versions
- update dependencies
- *(release)* bumped version to 0.2.4

## [0.2.3] - 2026-02-17

### 🚀 Features

- *(template)* cleaner justfile
- *(template)* add optional flags to the test recipes

### 📚 Documentation

- update content

### 🧪 Testing

- update justfile rendering
- update justfile rendering

### 💼 Other

- *(claude)* add context for claude code
- apply the template on it self
- *(release)* bumped version to 0.2.3

## [0.2.2] - 2026-02-10

### 🚀 Features

- update contribugting guide

### 🐛 Bug Fixes

- add init recipe to gitignore
- init recipe runs hooks to incorporate changes into commit

### 📚 Documentation

- add a contributing guide
- add contributing guide to zensical

### 🧪 Testing

- update contributing rendering

### 💼 Other

- update pre-commit hooks
- add github issue templates
- update dependencies
- add cache to clean recipe
- format pyproject toml
- *(release)* bumped version to 0.2.2

## [0.2.1] - 2026-02-10

### 🚀 Features

- extract init recipe and make one-time only
- allow uv to set or bump the version in release

### 🐛 Bug Fixes

- changelog creation
- init recipe removal for different platforms
- release tag for changelog and add test

### 🧪 Testing

- update test cases

### 💼 Other

- improve release recipes
- *(release)* bumped version to 0.2.1

## [0.2.0] - 2026-02-05

### 🚀 Features

- feat!(template): remove goreleaser
- *(template)* add dependencie updating recipe
- *(template)* update pre-commit hooks
- *(template)* add release workflow for gitlab
- use conventional-commits in release recipes
- *(template)* use just recipe to run test

### 📚 Documentation

- remove goreleaser

### 🧪 Testing

- update coverage test
- remove goreleaser
- update justfile lines
- update gitlab rendering

### 💼 Other

- *(template)* use just taskrunner as entrypoint to tests
- *(template)* update the trigger events
- add dependencie update recipe
- update pre-commit hooks and dependencies
- updated changelog
- bumped version to 0.2.0

## [0.1.13] - 2026-02-03

### 🚀 Features

- add pyproject format hook
- improved release recipe

### 🚜 Refactor

- set initial version to 0.0.0
- set use_goreleaser default to false

### 🧪 Testing

- update test cases
- update test case for justfile

### 💼 Other

- update pre-commit hooks
- update recipes
- format pyproject toml with hook
- format template pyproject.toml
- merge pull request #19 from npikall/dependabot/uv/zensical-0.0.19
- merge pull request #20 from npikall/dependabot/uv/ruff-0.14.14
- merge pull request #18 from npikall/dependabot/uv/ty-0.0.14
- updated changelog
- bumped version to 0.1.13

## [0.1.12] - 2026-02-02

### 🚀 Features

- *(template)* add github release workflow
- *(copier)* add github workflow question
- *(copier)* select individual workflows
- *(template)* group just recipes

### 🐛 Bug Fixes

- *(copier)* choices for github workflows
- *(template)* rendering in release workflow

### 🚜 Refactor

- make tests more readable

### 🧪 Testing

- add multiselect answer for github workflows
- update line numbers for new justfile

### 💼 Other

- run deployment of docs only when changed
- group just recipes
- fix commit message in recipe
- updated changelog
- bumped version to 0.1.12

## [0.1.11] - 2026-01-30

### 🐛 Bug Fixes

- *(template)* exclude docs files when not used

### 📚 Documentation

- add just install guide
- add clickable tasklist

### 🧪 Testing

- correct files get excluded when no docs defined

### 💼 Other

- merge pull request #13 from npikall/dependabot/uv/ruff-0.14.11
- merge pull request #14 from npikall/dependabot/uv/ty-0.0.11
- merge pull request #15 from npikall/dependabot/uv/ruff-0.14.13
- merge pull request #16 from npikall/dependabot/uv/ty-0.0.12
- merge pull request #17 from npikall/dependabot/uv/zensical-0.0.17
- update recipe, for smoother release recipe
- updated changelog
- bumped version to 0.1.11
- add release workflow

## [0.1.10] - 2026-01-09

### 🚀 Features

- *(template)* add mkdocstrings configuration for nicer api references

### 🐛 Bug Fixes

- *(release)* add v to version tag in changelog

### 💼 Other

- updated changelog
- bumped version to 0.1.10

## [0.1.9] - 2026-01-08

### 🐛 Bug Fixes

- changelog
- whitespaces at end of line

### 🧪 Testing

- refactor to table driven test

### 💼 Other

- update changelog
- updated changelog
- bumped version to 0.1.9

## [0.1.8] - 2026-01-08

### 🚀 Features

- *(template)* add mkdocstrings and api reference
- add changelog to docs
- add contributing to docs
- add license to docs
- update docs index to use readme

### 📚 Documentation

- added goreleaser, prek and changelog
- update color scheme
- fix index icon
- update, add license and changelog

### 🚜 Refactor

- add default config of zensical

### 🧪 Testing

- add typehints to useranswer model
- update for next version

### 💼 Other

- merge pull request #9 from npikall/feat-docs

docs: added goreleaser, prek and changelog
- merge pull request #11 from npikall/dependabot/uv/zensical-0.0.15

chore(deps-dev): bump zensical from 0.0.14 to 0.0.15
- merge pull request #10 from npikall/dependabot/uv/ty-0.0.8

chore(deps-dev): bump ty from 0.0.6 to 0.0.8
- update dev dependencies
- change default docs engine

## [0.1.7] - 2025-12-25

### 🐛 Bug Fixes

- remove whitespace at end-of-line

### 💼 Other

- updated changelog
- bumped version to 0.1.7

## [0.1.6] - 2025-12-25

### 🚀 Features

- *(template)* added goreleaser config
- prompt for optional goreleaser
- added a mit license
- added mkdocs option
- added changelog
- *(template)* added changelog
- *(template)* added mkdocs

### 🐛 Bug Fixes

- *(justfile)* actually push relase to remote
- *(justfile)* run tests before release

### 🧪 Testing

- check for goreleaser file
- added test for docs
- added changelog to file list

### ◀️ Revert

- removed latest version from changelog

### 💼 Other

- update justfile
- added release recipe
- updated changelog
- bumped version to 0.1.6

## [0.1.5] - 2025-12-24

### 🚀 Features

- *(template)* update pre-commit config
- *(template)* added issue templates
- *(template)* added optional prek as pre-commit
- switched to prek

### 📚 Documentation

- update to account for prek

### 🧪 Testing

- added jinja tags check
- refactor answer model

### 💼 Other

- added other ci file
- merge pull request #7 from npikall/dependabot/uv/ruff-0.14.10

chore(deps-dev): bump ruff from 0.14.9 to 0.14.10
- merge pull request #6 from npikall/dependabot/uv/ty-0.0.6

chore(deps-dev): bump ty from 0.0.3 to 0.0.6
- merge pull request #5 from npikall/dependabot/uv/zensical-0.0.14

chore(deps-dev): bump zensical from 0.0.11 to 0.0.14
- merge pull request #8 from npikall/feat-prek

add jinja tag test and switch to prek

## [0.1.4] - 2025-12-18

### 🚀 Features

- added pre-commit hook

### 🐛 Bug Fixes

- typos and unused jinja tags
- removed unused noqa

### 📚 Documentation

- update and added 'update' section

### 🧪 Testing

- added initial tests
- improved testing

### 💼 Other

- update files
- added ci checks

## [0.1.3] - 2025-12-14

### 🐛 Bug Fixes

- none license case

## [0.1.2] - 2025-12-13

### 🐛 Bug Fixes

- optinal files and directories

### 📚 Documentation

- fix links
- added documenatation
- added docs config
- added content

### 💼 Other

- added documentation publishing
- update project files

## [0.1.1] - 2025-12-12

### 📚 Documentation

- update readme
- update both readme's

## [0.1.0] - 2025-12-12

### 🚀 Features

- added files
- added cookiecutter functionality
- added cookiecutter json
- added ci workflows
- added pre/post hooks
- added docs
- populated src and test dirs
- changed from conda to uv
- updated prompts
- *(ci)* added automated tests and publishing workflows
- added optional licenses
- added ci recipes
- pinned python version
- added contributing guidelines
- added dev dependencies
- added rich success message
- moved tagging into separate recipe
- [**breaking**] added automatic python version
- added dynamic python version
- add dependabot with uv
- added pre-commit hooks
- *(just)* add documentation serve recipe
- added test coverage
- add zensical as dependencie
- make recipe 'tag' public
- restructure for copier
- added updating capability

### 🐛 Bug Fixes

- *(ci)* copy without render
- jinja extensions
- python version
- jinja variables
- jinja variables
- python version variables
- jinja variable of src/module
- minor bugs

### 📚 Documentation

- updated readme
- added default badges
- added reference to python handbook
- removed duplicated read more remarks
- update readme
- fix typos

### 🚜 Refactor

- moved to uv run
- simplified processes

### ◀️ Revert

- update python in template
- removed unused dependencies

### 💼 Other

- first commit
- expanded justfile commands
- excluded justfile from rendering
- updated justfile
- run pytest in uv venv
- added trigger
- disabled smoke-tests and publish
- added major operating systems to matrix
- added dependencies and configs
- moved file ignores to pyproject.toml
- pinned dev dependencies

[0.2.7]: https://github.com/npikall/py-bootstrap/compare/v0.2.6..0.2.7
[0.2.6]: https://github.com/npikall/py-bootstrap/compare/v0.2.5..v0.2.6
[0.2.5]: https://github.com/npikall/py-bootstrap/compare/v0.2.4..v0.2.5
[0.2.4]: https://github.com/npikall/py-bootstrap/compare/v0.2.3..v0.2.4
[0.2.3]: https://github.com/npikall/py-bootstrap/compare/v0.2.2..v0.2.3
[0.2.2]: https://github.com/npikall/py-bootstrap/compare/v0.2.1..v0.2.2
[0.2.1]: https://github.com/npikall/py-bootstrap/compare/v0.2.0..v0.2.1
[0.2.0]: https://github.com/npikall/py-bootstrap/compare/v0.1.13..v0.2.0
[0.1.13]: https://github.com/npikall/py-bootstrap/compare/v0.1.12..v0.1.13
[0.1.12]: https://github.com/npikall/py-bootstrap/compare/v0.1.11..v0.1.12
[0.1.11]: https://github.com/npikall/py-bootstrap/compare/v0.1.10..v0.1.11
[0.1.10]: https://github.com/npikall/py-bootstrap/compare/v0.1.9..v0.1.10
[0.1.9]: https://github.com/npikall/py-bootstrap/compare/v0.1.8..v0.1.9
[0.1.8]: https://github.com/npikall/py-bootstrap/compare/v0.1.7..v0.1.8
[0.1.7]: https://github.com/npikall/py-bootstrap/compare/v0.1.6..v0.1.7
[0.1.6]: https://github.com/npikall/py-bootstrap/compare/v0.1.5..v0.1.6
[0.1.5]: https://github.com/npikall/py-bootstrap/compare/v0.1.4..v0.1.5
[0.1.4]: https://github.com/npikall/py-bootstrap/compare/v0.1.3..v0.1.4
[0.1.3]: https://github.com/npikall/py-bootstrap/compare/v0.1.2..v0.1.3
[0.1.2]: https://github.com/npikall/py-bootstrap/compare/v0.1.1..v0.1.2
[0.1.1]: https://github.com/npikall/py-bootstrap/compare/v0.1.0..v0.1.1
[0.1.0]: https://github.com/npikall/py-bootstrap/tree/v0.1.0

<!-- generated by git-cliff -->
