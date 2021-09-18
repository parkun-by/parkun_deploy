SHELL := /bin/bash

restart_all: stop start

stop:
	docker-compose -f ~/deploy/docker-compose.yml down

start:
	docker-compose -f ~/deploy/docker-compose.yml up -d --build

venv:
	rm -rf .venv/
	python -m venv .venv; \
	( \
		source .venv/bin/activate \
		pip install --upgrade pip; \
		pip install --upgrade wheel; \
		pip install -r requirements.txt; \
	)
