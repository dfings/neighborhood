.PHONY: build clean run run_docker run_docker_image test venv

.DEFAULT_GOAL = run
.SHELLFLAGS = -ec

# Constants
APP_NAME = neighborhood

# Builds a local Docker image with pack.
build: clean
	pack build $(APP_NAME) \
		--path src \
		--builder gcr.io/buildpacks/builder:v1

# Deletes the __pycache__ directories.
clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

# Runs a local debug server.
run:
	. .venv/bin/activate; \
	cd src; \
	uvicorn server:app --reload --port 5001

# Builds and runs a local Docker image.
run_docker: build run_docker_image

# Runs a local Docker image.
run_docker_image:
	docker run --rm -it -p 8080:8080 $(APP_NAME)

test:
	. ./.venv/bin/activate; \
	pytest -vv; \
	mypy --strict --allow-untyped-decorators --ignore-missing-imports src; \
	ruff check src

# Sets up the virtual environment.
venv:
	uv venv --clear; \
	uv pip install -r src/requirements.txt; \
	uv pip install -r src/requirements-test.txt
