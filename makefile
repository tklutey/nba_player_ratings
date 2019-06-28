test:
	coverage run --branch --source=src/ -m unittest discover tst/
	coverage report
