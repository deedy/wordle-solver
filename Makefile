.PHONY: test

test:
	python3 -m unittest

cover:
	coverage run -m unittest discover && coverage report

cover-html:
	coverage run -m unittest discover && coverage html -d htmlcov && open htmlcov/index.html