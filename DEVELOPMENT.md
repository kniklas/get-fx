# Development specific instructions

Related to setting up development environment and potential troubleshooting hints.

## Branches

### Master (protected)

Use for production releases of documentation and package.
- 'production' version of the documentation: [https://kniklas.github.io/get-fx/](https://kniklas.github.io/get-fx/) (published to `gh-pages` branch of this repository)

### Dev (protected)

Use for staging (testing) releases of:
- documentation: [https://kniklas.github.io/pages-staging/getfx/](https://kniklas.github.io/pages-staging/getfx/)  (published to [documentation staging repository](https://github.com/kniklas/pages-staging))
- python package: [https://test.pypi.org/project/getfx/](https://test.pypi.org/project/getfx/)

### Feature branches

Use for development of specific feature or fix. Each feature branch must have created Pull Request.


## Building

This project assumes you have installed `make` on your operating system. If you wish to use different building tool please do this on your fork and do not merge to upstream unless agreed with project owner. Please note `make` rules are used not only a handy tool during development to automate building, cleanup, testing but as well by GitHub Actions workflows.


## pyenv

You can use different python versions / packages manager, but then **tox related matrix testing** will not work out of box (as currently implemented in `Makefile`). In such case you would have to write your own makefile rules or use different building tool.

Install [pyenv](https://github.com/pyenv/pyenv).

Make sure you have installed required python versions in `pyenv` (which python versions? Check `tox.ini` and `Makefile`):
* `cd $(pyenv root) && git pull` - update python versions in pyenv
* `pyenv install --list` - List all available for installation python versions
* `pyenv install <python-version>` - specify version avaialble for install. Note installation might take a while

Now you need to create virtual environment with specific python version.  Ideally install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) and then create virutal environment using specific python version:
* `pyenv virtualenv <python version> <name of environment>` - create virtual environment for specific python version available in pyenv
*  `pyenv activate <name of environment>` or `pyenv shell <name of environment>`- to activate
*  `pyenv deactivate` or `pyenv shell system` - to deactivate
*  `pyenv uninstall my-virtual-env` or `pyenv delete my-virtual-env` - to
   remove
* `pyenv virtualenvs` - to list all environments

Best if you define specific python version / virtual environment in `.python-version` - see below chapter for more details.


### .python-version

* `pyenv local <python-version>` - it creates or modifies `.python-version` in the directory! This file will contain python version name.

* `.python-version` file must match the name of an existing directory in ~/.pyenv/versions/. You can see the list of installed Python versions with pyenv versions.

**Note**: using `pyenv local <name of environment>` will switch to this virtual environment and set local virtual environment for this directly (will modify `.python-version`)

* removing `.python-version` will set the directly to the global python version (if python version was set)


### Tox and pyenv

If you wish to use `make tox` to test multiple versions with `pyenv` please bear following in mind:
* make sure you read how to use and what is impact of `pyenv local`, `pyenv global`, `pyenv shell` - see [documentation](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local)
* use with caution `pyenv shell` as this may destabilise `make tox` and/or `pyenv`
* use decent shell (e.g. [oh my zsh](https://ohmyz.sh) with pyenv plugins) to display virtual environment and/or actual python version
* look at [tox-pyenv-package](https://pypi.org/project/tox-pyenv/) for examples how to use pyenv and tox


## Dependencies

Required to build package: `pip3 install setuptools`.

There are three files where package dependencies are defiend:
* `requirements-build.txt` - packages required to build / run software from the code without tests (minimum). This must be in sync with `setup.py` -> `required_install`
* `requirements-test.txt` - additional packages required for running tests
* `requirements-dev.txt` - additional packages required to develop, debug software. In order to have complete development environment all three requirements files must be installed.

Do not use `pip3 freeze > requirements.txt` - as the dump is very long and might contain unecessary packages!

`pip3 install -r requirements-build.txt` - to install required minimum of packages required to run softare from the code.

If you wish to remove all packages, use: `pip freeze | xargs pip uninstall -y` [stack overflow](https://stackoverflow.com/a/11250821)


## Testing

In order to test if tool works correctly from command line use command: `make
test`, it will invoke three requests to NBP API with various command line
attributes.

Unit tests should be executed using `pytest` command, or checked constantly
during development using `ptw` (pytest watch).

### Testing multiple python versions

Do not use `tox` command as you may get failure that given python version is missing. In order to perform testing on multiple python versions use `make tox` instead.


### Testing using multiple Python versions

It has been verified that it is possible to use testing matrix from github actions from Python version 3.4. However replication of this testing using tox locally hit problems when building a package after `make clean` command is invoked. Specifically this error was raised: `FileNotFoundError: [Errno 2] No such file or directory: 'README.md'`.

In the future it might be considered to use tox support for following python versions:
* 3.4.2 - Debian 8 Jessie (2015 - 2018)
* 3.5.3 - Debian 9 Stretch (2017 - )
