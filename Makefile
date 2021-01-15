test:
	python3 getfx
	python3 getfx USD
	python3 getfx GBP -d 2020-11-27

test-cov:
	coverage run -m --source=getfx/ -m pytest
	coverage report -m

build:
	python3 setup.py sdist bdist_wheel

build-clean:
	rm -rf dist/ get_fx_kniklas.egg-info/ build/

build-test:
	pip install -e .
	python3 -m getfx USD

requirements:
	pip3 freeze > requirements.txt
	git st requirements.txt
	git diff requirements.txt
