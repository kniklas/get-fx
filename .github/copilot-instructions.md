# Copilot Instructions for GetFX

## Build, Test, and Lint Commands

### Building the Package

- **`make build`**: Complete build process (installs dependencies, builds docs, creates wheel and sdist packages, installs package in editable mode)
- **`make install-dependencies`**: Installs all dependencies from requirements files (build, test, and dev)

### Testing

- **`pytest`**: Run unit tests in `tests/` directory
- **`pytest tests/test_getfxnbp.py`**: Run a specific test file
- **`pytest tests/test_getfxnbp.py::test_function_name`**: Run a specific test
- **`make tests`**: Run full test suite with linting (runs lint, then pytest)
- **`make test-cov`**: Run tests with coverage report
- **`make test-e2e`**: Run end-to-end tests against actual NBP API (no mocking)

### Linting and Code Quality

- **`make lint`**: Run all linters (flake8, black, yamllint)
- **`flake8 .`**: Check code style (max line length 79 chars enforced)
- **`black . -l 79 --check`**: Check black formatting (79 char line limit)
- **`python -m yamllint <file.yml>`**: Check YAML formatting

### Testing Multiple Python Versions

- **`make tox`**: Test against all Python versions defined in `tox.ini` (3.7.3, 3.8.5, 3.9.0) using pyenv
  - Requires: `pyenv` installed with specified Python versions
  - Requires: `.python-version` file set to a pyenv virtual environment name (not direct versions)

### Cleaning

- **`make clean`**: Remove build artifacts, cache, and temporary files

## Architecture Overview

GetFX is a Python CLI tool to download FX rates from the National Bank of Poland (NBP) API. It's designed with extensibility in mind for supporting multiple FX providers.

### Core Design Pattern: Template Method

The codebase follows a **template method pattern** for FX provider implementations:

1. **`getfx.GetFX`** (`src/getfx/getfx.py`): Abstract base class defining protected methods and attributes for any FX provider
   - Protected attributes: `_currency_code`, `_table_number`, `_effective_date`, `_rate`
   - Protected methods: `_delete()`, `_set_currency()`, `_set_table()`, `_set_rate()`, `_set_effective_date()`
   - Subclasses must override and implement the interface

2. **`getfx.getfxnbp.GetFxNBP`** (`src/getfx/getfxnbp.py`): NBP API-specific implementation
   - Extends `GetFX` with public methods for NBP operations
   - Uses `NBP_API_URL` constant for API endpoint
   - Makes HTTP requests using `requests` library
   - Parses JSON responses and validates data

3. **`getfx.cmdparser`** (`src/getfx/cmdparser.py`): CLI argument parsing
   - Defines `DEFAULT_CURRENCY` (CHF)
   - `parse_getfx()` function uses argparse to parse command-line arguments
   - Arguments: currency code (optional), date flag (`-d` or `--date`)

4. **Entry Point**: `getfx.getfxnbp.init_cmd()` is the console script entry point
   - Parses arguments, creates `GetFxNBP` instance, executes operations

### Dependency Management

Three separate requirements files with specific purposes:
- **`requirements-build.txt`**: Minimum runtime dependencies (must sync with `setup.py` `install_requires`)
- **`requirements-test.txt`**: Additional packages for unit testing
- **`requirements-dev.txt`**: Additional packages for development and documentation

All three are installed with `make install-dependencies` for a complete dev environment.

### Documentation

- Generated with Sphinx from RST docstrings in source code
- Built to `docs/build/html/` via `make docs`
- Docstrings follow RST format and are published under "Source documentation" section
- GitHub Actions publishes to gh-pages on version tags

## Key Conventions

### Version Management

- Single source of truth: `src/getfx/__init__.py` contains:
  - `__version__`: Package version (e.g., "0.1.8")
  - `__minPythonVersion__`: Minimum Python version (e.g., "3.7")
- Version must match git tag when releasing (e.g., tag `v0.1.8` for version "0.1.8")
- Use `make add-ver` to automatically create version tag from `__version__`

### Code Style

- **Line length**: Maximum 79 characters (enforced by flake8 and black)
- **Formatter**: black with `-l 79` flag
- **Linter**: flake8
- **YAML**: yamllint validation

### Testing Requirements

- All functional changes must have corresponding unit tests
- Pull requests without unit tests are rejected
- Use `pytest` for test execution
- Each test file follows pattern: `test_<module_name>.py`
- Tests can be run individually with pytest selectors

### Python Version Support

- Minimum: Python 3.7 (from `__minPythonVersion__`)
- Currently tested against: 3.7.3, 3.8.5, 3.9.0 (defined in `tox.ini`)
- Use pyenv + tox for local testing across versions

### Git Conventions

- **Protected branches**: `master` (use for production releases)
- **Feature branches**: Non-protected; must have Pull Request
- **Commits**: No squashing on protected branches; squash only on feature branches
- **Tags**: Version tags published to trigger GitHub Actions (staging: `v*-dev*`, production: stable versions without `-dev`)

### Docstring Format

- Use RST docstring format for automatic documentation generation
- Example from `cmdparser.py`:
  ```python
  def parse_getfx(test_args=None):
      """Initialize argparse parser and return parsed arguments.

      :keyword test_args: Used for unit testing (None for real usage)
      :returns: Namespace object with parsed arguments
      """
  ```

### Entry Points and Execution

- Console script entry point: `getfx = getfx.getfxnbp:init_cmd`
- Command-line usage: `getfx [CURRENCY] [-d DATE]` or `python3 -m getfx`
- Example: `getfx USD -d 2020-10-03` retrieves USD rate for October 3, 2020

## NBP API Integration

- **URL**: `http://api.nbp.pl/api/exchangerates/rates/A`
- All rates are in Polish Złoty (PLN)
- Default currency: CHF (Swiss Franc)
- Date format: YYYY-MM-DD
- Make HTTP requests using `requests` library
- Handle API errors and validate responses appropriately
