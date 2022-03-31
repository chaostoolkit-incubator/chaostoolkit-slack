.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python setup.py develop

.PHONY: lint
lint:
	flake8  chaosslack/ tests/
	isort --check-only --profile black  chaosslack/ tests/
	black --check --diff --line-length=80 chaosslack/ tests/

.PHONY: format
format:
	isort --profile black  chaosslack/ tests/
	black --line-length=80 chaosslack/ tests/

.PHONY: tests
tests:
	pytest
