VERSIONS = 3.7.3 3.8.5 3.9.0
PYENV := $(shell pyenv local)
PUBLISH_PROD_URL = kniklas.github.io
PUBLISH_TEST_URL = kniklas.github.io/getfx-test/
CP_RM_FLAGS = -vrf
PACKAGE_VER := $(shell cat src/getfx/__init__.py \
	| grep version \
	| awk -F"= " '{ print $$2 }'\
	| sed 's/"//g')

show-ver:
	@echo Get FX version: $(PACKAGE_VER) 2> /dev/null

test-e2e:
	python3 -m getfx
	python3 -m getfx USD
	python3 -m getfx GBP -d 2020-11-27

test-cov:
	coverage run -m --source=src/ -m pytest
	coverage report -m

test-cov-pub: test-cov
	coveralls

tests: clean
	pytest
	flake8 .

docs: clean
	sphinx-build -a -b html docs/source docs/build/html

all: tests test-cov build

build: docs
	@echo BUILDING PACKAGE
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	pip install -e .

install-dependencies:
	pip install -r requirements-build.txt
	pip install -r requirements-test.txt
	pip install -r requirements-dev.txt

remove-dependencies:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

tox: python
	pip install tox tox-pyenv
	pip install -U pip
	pyenv local $(VERSIONS)
	tox
	pyenv local $(PYENV)

# Commented as publishing preferably should be done via GitHub action
# publish: doc
#     @echo ===== PUBLISHING =====
#     mkdir -pv ../$(PUBLISH_PROD_URL)
#     cd ../$(PUBLISH_PROD_URL) && git checkout master && git pull
#     rm $(CP_RM_FLAGS) ../$(PUBLISH_PROD_URL)/getfx/*
#     cp $(CP_RM_FLAGS) docs/build/html/* ../$(PUBLISH_PROD_URL)/getfx
#     cd ../$(PUBLISH_PROD_URL) \
#         && git add . \
#         && git commit -m "Update web page for package version: $(PACKAGE_VER)" \
#         && git push

push-pypi: build
	python3 -m twine upload --repository testpypi --skip-existing dist/*

python:
	for i in $(VERSIONS); do \
		pyenv install -s $i; \
	done

clean:
	rm $(CP_RM_FLAGS) \
		src/getfx/*.html \
		dist \
		build \
		getfx \
		.pytest_cache \
		docs/build \
		.eggs
	rm -fv docs/*.html
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type d -name getfx.egg-info -exec rm -r {} \+
