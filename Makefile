SHELL=/bin/bash -euo pipefail

install-python:
	poetry install

install-node:
	npm install --legacy-peer-deps

.git/hooks/pre-commit:
	cp scripts/pre-commit .git/hooks/pre-commit

install: install-node install-python .git/hooks/pre-commit

lint:
	npm run lint
	find . -name '*.py' -not -path '**/.venv/*' | xargs poetry run flake8 --ignore=E501

clean:
	rm -rf build
	rm -rf dist

publish: clean
	mkdir -p build
	npm run publish 2> /dev/null

serve:
	npm run serve

check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh

format:
	poetry run black **/*.py

start-sandbox:
	cd sandbox && npm run start

build-proxy:
	scripts/build_proxy.sh

_dist_include="poetry.lock poetry.toml pyproject.toml Makefile build/."

release: clean publish
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done

test:
	@echo no tests for spec-only API
