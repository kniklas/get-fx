# Development specific instructions

Related to setting up development environment and potential troubleshooting
hints.

## Raising issues

In general you are welcomed to raise or comment any issue. Only exception is
for items which are more ideas that require discussion. It may happen that some
issues will be closed or followed in discussion - especially if they are very
tricky items for implementation or not sure if given change will be
implemented. In case of doubt you can always raise new issue.

Topics that most likely will be not converted to discussion are:
- bugs
- new features / enhancements


## Branches, releasing and versions

Protected branches should not have squashed commits! Squash commits is allowed
only on features branches.

### Master (protected)

Use for production releases of documentation and package.
- 'production' version of the documentation:
  [https://kniklas.github.io/get-fx/](https://kniklas.github.io/get-fx/)
  (published to `gh-pages` branch of this repository)

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

**Note**: avoid feature branches with `dev` or `mas` characters in name, as
they will be treated as protected branch!

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
3. Before finishing PR and submitting for review, squach all committs using
   GitHub _Squash and merge_ or squach all commits on feature branch locally.
4. When work on pull request is finished, before merging it to upstream branch
   make sure version in `src/getfx/__init__.py` is set to new version.
5. After the pull request is merged to upstream branch push new tag which is
   the same as package version, ideally using `make add-ver` - this rule will
   automatically take package version to set-up local and remote tag (not
   annotated).

#### Manual publishing (using make)

As alternative way to publish a package using: `make push-pypi-test` or `make
push-pypi-prod`. This can be used if for some reason workflow actions should
not be used or they are not working correctly. In such case please remember to
apply version tag to commit which is used for new version.

In order to perform manual publishing you need to have valid pypi API tokens
stored in `~/.pypirc` configuration file.


## Building

This project assumes you have installed `make` on your operating system. If you
wish to use different building tool please do this on your fork and do not
merge to upstream unless agreed with project owner. Please note `make` rules
are used not only a handy tool during development to automate building,
cleanup, testing but as well by GitHub Actions workflows.


## Commits

1. Ideally use short / atomic commits for specific feature
2. Follow [50/72 rule](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) for writing commits
3. You can invoke `make build` or `make docs` locally in case of doubt or if
   local troubleshooting is required.


## pyenv

You can use different python versions / packages manager, but then **tox
related matrix testing** will not work out of box (as currently implemented in
`Makefile`). In such case you would have to write your own makefile rules or
use different building tool.

Install [pyenv](https://github.com/pyenv/pyenv).

Make sure you have installed required python versions in `pyenv` (which python
versions? Check `tox.ini` and `Makefile`):
* `cd $(pyenv root) && git pull` - update python versions in pyenv
* `pyenv install --list` - List all available for installation python versions
* `pyenv install <python-version>` - specify version avaialble for install.
  Note installation might take a while

Now you need to create virtual environment with specific python version.
Ideally install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
and then create virutal environment using specific python version:
* `pyenv virtualenv <python version> <name of environment>` - create virtual
  environment for specific python version available in pyenv
*  `pyenv activate <name of environment>` or `pyenv shell <name of
   environment>`- to activate
*  `pyenv deactivate` or `pyenv shell system` - to deactivate
*  `pyenv uninstall my-virtual-env` or `pyenv delete my-virtual-env` - to
   remove
* `pyenv virtualenvs` - to list all environments

Best if you define specific python version / virtual environment in
`.python-version` - see below chapter for more details.


### .python-version

* `pyenv local <python-version>` - it creates or modifies `.python-version` in
  the directory! This file will contain python version name.

* `.python-version` file must match the name of an existing directory in
  ~/.pyenv/versions/. You can see the list of installed Python versions with
  pyenv versions.

**Note**: using `pyenv local <name of environment>` will switch to this virtual
environment and set local virtual environment for this directly (will modify
`.python-version`)

* removing `.python-version` will set the directly to the global python version
  (if python version was set)


### Tox and pyenv

If you wish to use `make tox` to test multiple versions with `pyenv` please
bear following in mind:
* make sure you read how to use and what is impact of `pyenv local`, `pyenv
  global`, `pyenv shell` - see
  [documentation](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local)
* use with caution `pyenv shell` as this may destabilise `make tox` and/or
  `pyenv`
* use decent shell (e.g. [oh my zsh](https://ohmyz.sh) with pyenv plugins) to
  display virtual environment and/or actual python version
* look at [tox-pyenv-package](https://pypi.org/project/tox-pyenv/) for examples
  how to use pyenv and tox


## Dependencies

Required to build package: `pip3 install setuptools`.

There are three files where package dependencies are defiend:
* `requirements-build.txt` - packages required to build / run software from the
  code without tests (minimum). This must be in sync with `setup.py` ->
  `required_install`
* `requirements-test.txt` - additional packages required for running tests
* `requirements-dev.txt` - additional packages required to develop, debug
  software. In order to have complete development environment all three
  requirements files must be installed.

Do not use `pip3 freeze > requirements.txt` - as the dump is very long and
might contain unecessary packages!

`pip3 install -r requirements-build.txt` - to install required minimum of
packages required to run softare from the code.

If you wish to remove all packages, use: `pip freeze | xargs pip uninstall -y`
[stack overflow](https://stackoverflow.com/a/11250821)


## Testing

In order to test if tool works correctly from command line use command: `make
test`, it will invoke three requests to NBP API with various command line
attributes.

Unit tests should be executed using `pytest` command, or checked constantly
during development using `ptw` (pytest watch).

### Testing multiple python versions

Do not use `tox` command as you may get failure that given python version is
missing. In order to perform testing on multiple python versions use `make tox`
instead.


### Testing using multiple Python versions

It has been verified that it is possible to use testing matrix from github
actions from Python version 3.4. However replication of this testing using tox
locally hit problems when building a package after `make clean` command is
invoked. Specifically this error was raised: `FileNotFoundError: [Errno 2] No
such file or directory: 'README.md'`.

In the future it might be considered to use tox support for following python
versions:
* 3.4.2 - Debian 8 Jessie (2015 - 2018)
* 3.5.3 - Debian 9 Stretch (2017 - )
