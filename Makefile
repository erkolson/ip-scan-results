


.PHONY: test run setup

setup:
	./scripts/dev_setup.sh

run:
	python ip-scan-results.py

test:
	python -m test.db_test
