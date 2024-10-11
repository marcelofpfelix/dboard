# Makefile

################################################################################
# variables
name := dboard
app_args := -c config.yml

python_version := 3.11

################################################################################
# targets
################################################################################

.EXPORT_ALL_VARIABLES:
.ONESHELL:
.PHONY: all clean test env venv
SHELL := bash
.DEFAULT_GOAL := app

################################################################################
# python
################################################################################

env: venv dep ## create venv and install dependencies locally

venv:
	pyenv install $(python_version) -s
	pyenv local $(python_version)
	rm -rf .env
	python3 -m venv .env

dep:
	source .env/bin/activate
	pip install --upgrade pip
	pip install --requirement requirements-dev.txt
	echo "\nDon't forget to run manually: \n\n
	source .env/bin/activate"

app: ## run app locally
	uv run python3 -m $(name) $(app_args)

pre: ## run pre-commit
	pre-commit run --all-files

check: ## run check scripts
	ci/quality.sh
	ci/test.sh

# requires uv
req: ## update requirements.txt
	uv sync
	uv export -f requirements.txt --output requirements.txt --without-hashes
	uv export --dev -f requirements.txt --output requirements-dev.txt --without-hashes

test: ## run pytest
	coverage run -m pytest tests
	coverage combine
	coverage report --show-missing

.ONESHELL:
bin: ## create binary file
	docker run --rm --name pyinstaller -v "$(shell pwd):/src/" cdrx/pyinstaller-linux "pyinstaller -F dboard/main.py -n dboard"

.ONESHELL:
lint: ## lint code
	python3 -m ruff check $(name)/* tests --fix
	python3 -m black $(name) tests
	python3 -m mypy $(name) tests --strict

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s:\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\asd033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
