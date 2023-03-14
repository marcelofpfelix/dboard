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
	pip install --upgrade pip

dep:
	source .env/bin/activate
	pip install --upgrade pip-tools
	pip install --requirement requirements.txt

app: ## run app locally
	python3 -m $(app) $(app_args)

# requires poetry
req: ## update requirements.txt
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.ONESHELL:
lint:
	flake8 $(app)/*
	pylint $(app)/*

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s:\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\asd033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
