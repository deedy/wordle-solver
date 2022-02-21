.PHONY: test

test:
	python3 -m unittest

cover:
	coverage run -m unittest discover && coverage report

cover-report:
	coverage run -m unittest discover && coverage html -d htmlcov && open htmlcov/index.html