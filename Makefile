VERSIONS = 3.7.3 3.8.5 3.9.0
PYENV := $(shell pyenv local)

test:
	python3 -m getfx
	python3 -m getfx USD
	python3 -m getfx GBP -d 2020-11-27

test-cov:
	coverage run -m --source=src/ -m pytest
	coverage report -m

build: clean
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	pip install -e .

clean:
	rm -vrf \
		dist/ \
		build/ \
		getfx/getfx.egg-info/ \
		getfx.egg-info/ \
		src/getfx.egg-info/ \
		get_fx_kniklas.egg-info/

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

python:
	for i in $(VERSIONS); do \
		pyenv install -s $i; \
	done
