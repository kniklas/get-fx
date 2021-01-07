# get-fx

Get FX is tool to download average FX rates from National Bank of Poland (NBP)

![](https://github.com/kniklas/get-fx/workflows/build/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/kniklas/get-fx/badge.svg?branch=master&t=xgdvqo)](https://coveralls.io/github/kniklas/get-fx?branch=master)


# Usage

`python3 getfx` - basic usage with default currency and today date
`python3 getfx -h|--help` - display help


# Development specific instructions

## pyenv

Install [pyenv](https://github.com/pyenv/pyenv).

Make sure you have installed python version in `pyenv`:
* `cd $(pyenv root) && git pull)` - update python versions in pyenv
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


## pip3

`pip3 freeze > requirements.txt` - to dump the requirements
`pip3 install -r requirements.txt` - to install as per requirements


## testing

In order to test if tool works correctly from command line use command: `make
test`, it will invoke three requests to NBP API with various command line
attributes.

Unit tests should be executed using `pytest` command, or checked constantly
during development using `ptw` (pytest watch).
