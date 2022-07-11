SHELL := /bin/bash
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))

list:
	@grep '^[^#[:space:]].*:' Makefile

build:
	cp -R ../specification .
	docker build --network=host .

clean:
	rm -rf ./node_modules

install:
	npm install --dev

update:
	npm update

test:
	npm test

test-report:
	NODE_ENV=test npx mocha --reporter mocha-junit-reporter --reporter-options mochaFile=../reports/tests/$(dirname).xml || true