test:
	python3 -m unittest

cover:
	coverage run -m unittest discover >& /dev/null && coverage report

cover-report:
	coverage run -m unittest discover >& /dev/null && coverage html -d htmlcov && open htmlcov/index.html