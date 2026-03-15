all: lint test

lint:
	uv run pylint $(shell git ls-files '*.py')

test:
	uv run pytest test_worder.py -v
