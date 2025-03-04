SOURCES = app tests

.DEFAULT_GOAL := help
py ?= python -m poetry run

DOCKER_COMPOSE_FILE = contrib/docker-compose.yml
DOCKER_COMPOSE_PROJECT_NAME = awo_generator


help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

install: ## Install project dependencies
	python -m poetry install --no-interaction --no-ansi
.PHONY: install

format: ## Format the source code
	$(py) ruff check --config pyproject.toml --fix $(SOURCES)
	$(py) ruff format --config pyproject.toml $(SOURCES)
.PHONY: format

lint: ## Lint the source code
	$(py) ruff check --config pyproject.toml  $(SOURCES)
.PHONY: lint

test: ## Run tests
	$(py) pytest -s -vvv
.PHONY: test

coverage: ## Run unit tests and check coverage
	$(py) coverage run -m pytest --cov=app tests
	$(py) coverage report  --precision=2 -m  # uncomment to matter: --fail-under=80
.PHONY: coverage

compose-up: ## Run the development server with docker-compose
	COMPOSE_PROJECT_NAME=${DOCKER_COMPOSE_PROJECT_NAME} docker compose -f ${DOCKER_COMPOSE_FILE} up --build --no-deps --remove-orphans -d --force-recreate
.PHONY: compose-up

compose-down: ## Stop the development server with docker-compose
	COMPOSE_PROJECT_NAME=${DOCKER_COMPOSE_PROJECT_NAME} docker compose -f ${DOCKER_COMPOSE_FILE} down --remove-orphans -v -t 0
.PHONY: compose-down

run-web: ## Run the web server
	$(py) gunicorn -w 1 -k uvicorn.workers.UvicornWorker \
		app.asgi:fastapi_app --bind 0.0.0.0:8000 --timeout 300 \
		--graceful-timeout 30 --log-level DEBUG
.PHONY: run-web