test:
	python3 getfx
	python3 getfx USD
	python3 getfx GBP -d 2020-11-27

test-cov:
	coverage run -m --source=getfx/ -m pytest
	coverage report -m
