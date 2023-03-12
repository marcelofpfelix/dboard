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

# Generated variables.
docker_build_args := \
	--build-arg GIT_COMMIT=$(shell git show -s --format=%H) \
	--build-arg GIT_COMMIT_DATE="$(shell git show -s --format=%ci)" \
	--build-arg IMAGE_NAME=$(name) \
	--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%T.%N%Z") \
	--build-arg BUILD_URL=$(BUILD_URL) \
	--build-arg VER_PYTHON=$(python_version) \
	--build-arg VER_PIP=$(pip_version)

image_tag := registry.docker.internal.bandonga.com/library/$(name):$(tag)
docker_run_args := \
  -p 6060:6060 \
	--env-file $(env_file)

################################################################################
# TARGETS
################################################################################

.EXPORT_ALL_VARIABLES:
.PHONY: build logs requirements.txt requirements_dev.txt
all: build run 
SHELL := bash
.DEFAULT_GOAL := build

################################################################################
# DOCKER

stop:
	@echo MAKE stop $(image_tag)
	-@docker rm -f $(name)
clean: stop
	@echo MAKE removing $(image_tag)
	-@docker rmi -f $(image_tag)
# needed by jenkins
build: ## docker build 
	@echo MAKE building $(image_tag)
	docker build $(docker_build_args) -t $(image_tag) .
run: stop #sec ## docker run
	@echo MAKE running $(image_tag)
	docker run -it --rm --name $(name) $(docker_run_args)  $(image_tag)
rund: stop sec
	@echo MAKE running $(image_tag)
	docker run -dit --rm --name $(name) $(docker_run_args)  $(image_tag)
manual: stop #sec
	@echo MAKE running $(image_tag)
	docker run -it --rm --name $(name) --entrypoint /bin/sh $(docker_run_args) $(image_tag)
exec:
	@echo MAKE exec $(image_tag)
	@docker exec -it $(name) bash
logs:
	@echo MAKE logs $(image_tag)
	@docker logs $(name)
# needed by jenkins
test:
	@echo MAKE test
	@echo "Not implemented"
sec:
	@echo MAKE testing $(image_tag)
	@trivy image --ignore-unfixed --exit-code 1 --severity CRITICAL $(image_tag)
docker_lint:
	@docker run --rm -i hadolint/hadolint < Dockerfile
push:
	docker push $(image_tag)

# DEVELOPMENT
# =======================================================

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

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage: \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s:\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\asd033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
