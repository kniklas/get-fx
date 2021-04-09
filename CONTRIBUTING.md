# Contributing

Welcome! I am very happy you are interested in contribution to the project! :-)

In order to keep it organized in consistent and quality manner I will ask you
to follow below guidelines. If you have questions about below contribution
rules please raise discussion item in [Contribution discussion
thread](https://github.com/kniklas/get-fx/discussions/33). If you would like to
raise idea related to contribution rules (changes or improvements) please use
[Ideas discussion
thread](https://github.com/kniklas/get-fx/discussions/categories/ideas).

If you are looking for instructions how to build package from the source please
read: [DEVELOPMENT.md](DEVELOPMENT.md)


## When raise issue and when discussion idea?

In general you are welcomed to raise or comment any issue. Only exception is
for items that are ideas which require discussion - especially if they are
tricky for implementation or not sure if given change could be implemented. In
such case use [Ideas discussion
category](https://github.com/kniklas/get-fx/discussions/categories/ideas). If
you are unsure if issue or idea discussion should be used, then start with idea
discussion first.

Examples what are valid issues (not discussion items):
- bugs
- valid (verified by repository owner) new features / enhancements


## Branches, releasing and versions

Protected branches should not have squashed commits! Squash commits are allowed
only on feature branches.

### Master (protected)

Use for production releases of documentation and package.
- 'production' version of the documentation:
  [https://kniklas.github.io/get-fx/](https://kniklas.github.io/get-fx/)
  (published to `gh-pages` branch of this repository)
- python package: [https://pypi.org/project/getfx/](https://pypi.org/project/getfx/)

### Dev (protected)

Use for staging (testing) releases of:
- documentation:
  [https://kniklas.github.io/pages-staging/getfx/](https://kniklas.github.io/pages-staging/getfx/)
  (published to [documentation staging
  repository](https://github.com/kniklas/pages-staging))
- python package:
  [https://test.pypi.org/project/getfx/](https://test.pypi.org/project/getfx/)

### Feature branches

Use for development of specific feature or fix. Each feature branch must have
created Pull Request.

**Note**: avoid feature branches with `dev` or `mas` characters in name, otherwise
they will be treated as protected branch!

### Pull requests

It is recommended in description of the pull request to list all key tasks /
features that are being implemented as task list. This allows easy tracking how
many tasks are completed and are outstanding. Additionally for each task please
provide reference to specific discussion or issue ID.

Note each pull request is validated using GitHub actions to check integrity of
the application. Each functional change which can be unit tested must have
written corresponding unit test. Pull requests which are not fulfilling this
criteria will be rejected.

### Releasing new versions (tags)

It is assumed that each new version (staging - from `dev` branch; production -
from `master` branch) is released by pushing a tag to given commit.

Depending on tag name convention, staging (`publish-dev.yml`) or production
(`publish-master.yml`) publish workflow is invoked:
- development versions: `v*-dev*` - for staging release - e.g. v0.1.2-dev2
- stable versions without: `-dev` for production release - e.g. v0.1.2

It is possible to push tag for code which is part of Pull Request or directly
push to given branch. There is no verification what is name of branch where the
tag is pushed! The only validation is to verify the tag name is the same as
package version stored in `src/getfx/__init__.py`.

#### Recommended practice

1. Work always on feature branches using Pull Request
2. Frequently push commit to feature branch - each commit is automatically
   tested
3. Before finishing PR and submitting for review, squash all commits using
   GitHub _Squash and merge_ or squash all commits on feature branch locally
   and force push to remote.
4. When work on pull request is finished, before merging it to upstream branch
   make sure version in `src/getfx/__init__.py` is set to new version.
5. After the pull request is merged to upstream branch push new tag which is
   the same as package version, ideally using `make add-ver` - this rule will
   automatically take package version to set-up local and remote tag (not
   annotated).

#### Manual publishing (using make)

It is possible to publish package to PyPI repository not via GitHub action but
from your computer using: `make push-pypi-test` or `make push-pypi-prod`.

This can be used if for some reason workflow actions should not be used or they
are not working correctly. In such case please remember to apply version tag to
commit which is used for new version.

In order to perform manual publishing you need to have valid PyPI API tokens
stored in `~/.pypirc` configuration file.


## Building

This project assumes you have installed `make` on your operating system. If you
wish to use different building tool please do this on your fork and do not
merge to upstream unless agreed with repository owner. Please note `make` rules
are used not only as handy tool during development to automate building,
cleanup, testing but as well by GitHub Actions workflows.


## Commits

1. Use short / atomic commits for specific feature
2. Follow [50/72 rule](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) for writing commits
3. You can invoke `make build` or `make docs` locally in case of doubt or if
   local troubleshooting is required.


## Testing

Make sure you write unit tests for each functional change that can be unit
tested. Pull requests without Unit Tests will be rejected. Each pull request is
automatically tested by building pipeline.

More on testing tools and approaches is provided in:
[DEVELOPMENT.md](DEVELOPMENT.md)


## Documentation

Document your code using RST docstrings as automatically generated
documentation publishes these docstrings under [Source
documentation](https://kniklas.github.io/get-fx/implementation/index.html)
section.

### Build documentation locally using make

It is recommended to run `make docs` to build locally documentation, so you can
check locally in folder: `docs/build/html`.  Additionally each time you invoke
`make build` this executes building documentation locally.

### Build documentation on GitHub Pages via GitHub actions

Each time commit is tagged with version tag starting from `v` character any
documentation changes will be published to GitHub pages using GitHub actions.
