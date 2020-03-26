SHELL := /bin/bash

restart_all: stop start

stop:
	docker-compose -f ~/deploy/docker-compose.yml down

start:
	docker-compose -f ~/deploy/docker-compose.yml up -d --build
