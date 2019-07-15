test:
	coverage run --branch --source=src/ -m unittest discover tst/
	coverage report

checkstyle:
	pycodestyle --max-line-length=120 --show-source .

backfill:
	python -m src.backfill.canonical_events
	python -m src.backfill.lineups.lineups
	python -m src.backfill.matchups

main:
	python -m src.activity.main

all: backfill main

release: checkstyle test
