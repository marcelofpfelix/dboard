# Makefile

################################################################################
# VARIABLES
name := dboard
app := dboard
tag := latest
app_args := -c config.yml

python_version := 3.11
pip_version := 21.3.1
env_file = local.env

################################################################################
# TARGETS
################################################################################

.EXPORT_ALL_VARIABLES:
.PHONY: logs requirements.txt requirements_dev.txt
SHELL := bash
.DEFAULT_GOAL := app

################################################################################
# DEVELOPMENT
################################################################################

env: venv dep ## create venv and install dependencies locally

venv:
	rm -rf .env
	python3 -m venv .env
	python3 -m pip install --upgrade pip

dep:
	source .env/bin/activate
	python3 -m pip install --upgrade pip-tools
	python3 -m pip install --requirement requirements-dev.txt

app: ## run app locally
	python3 -m $(app) $(app_args)

pre: ## run pre-commit
	pre-commit run --all-files

# requires poetry
req: ## update requirements.txt
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	poetry export --dev -f requirements.txt --output requirements-dev.txt --without-hashes

test: ## run pytest
	coverage run -m pytest tests
	coverage combine
	coverage report --show-missing

.ONESHELL:
bin: ## create binary file
	docker run --rm --name pyinstaller -v "$(shell pwd):/src/" cdrx/pyinstaller-linux "pyinstaller -F dboard/main.py -n dboard"

.ONESHELL:
lint: ## lint code
	python3 -m ruff check $(name)/* tests
	python3 -m black $(name) tests --check
	python3 -m mypy $(name) tests


help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s:\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\asd033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
