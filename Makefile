VERSIONS = 3.7.3 3.8.5 3.9.0
PYENV := $(shell pyenv local)
PUBLISH_REPO_URL = kniklas.github.io
CP_RM_FLAGS = -vrf
PACKGE_VER := $(shell cat src/getfx/__init__.py \
	| grep version \
	| awk -F"= " '{ print $$2 }'\
	| sed 's/"//g')

test-e2e:
	python3 -m getfx
	python3 -m getfx USD
	python3 -m getfx GBP -d 2020-11-27

test-cov:
	coverage run -m --source=src/ -m pytest
	coverage report -m

tests: clean
	pytest
	flake8 .

doc: clean
	sphinx-build -a -b html doc/source doc/build/html

all: tests test-cov build

build: doc
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
	pyenv local $(VERSIONS)
	pip install tox tox-pyenv
	pip install -U pip
	tox
	pyenv local $(PYENV)

publish: doc
	@echo ===== PUBLISHING =====
	cd ../$(PUBLISH_REPO_URL) && git checkout master && git pull
	rm $(CP_RM_FLAGS) ../$(PUBLISH_REPO_URL)/getfx/*
	cp $(CP_RM_FLAGS) doc/build/html/* ../$(PUBLISH_REPO_URL)/getfx
	cd ../$(PUBLISH_REPO_URL) \
		&& git add . \
		&& git commit -m "Update web page for package version: $(PACKGE_VER)" \
		&& git push

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
		doc/build \
		.eggs
	rm -fv doc/*.html
	find . -type d -name __pycache__ -exec rm -r {} \+
	find . -type d -name getfx.egg-info -exec rm -r {} \+
