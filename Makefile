deps:
	pip install -r requirements.txt

install-dev:
	pip install -e .

install:
	pip install .

test:
	pytest tests
