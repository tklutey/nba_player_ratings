test:
	coverage run --branch --source=src/ -m unittest discover tst/
	coverage report

checkstyle:
	pycodestyle --max-line-length=120 --show-source .

release: checkstyle test
