test:
	python3 getfx
	python3 getfx USD
	python3 getfx GBP -d 2020-11-27

test-cov:
	coverage run -m --source=getfx/ -m pytest
	coverage report -m

build:
	python3 -m pip install --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel

clean:
	rm -vrf dist/ getfx/getfx.egg-info/ getfx.egg-info/ get_fx_kniklas.egg-info/ build/

build-test:
	pip install -e .

requirements:
	pip3 freeze > requirements.txt
	git st requirements.txt
	git diff requirements.txt
