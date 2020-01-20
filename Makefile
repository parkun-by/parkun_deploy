SHELL := /bin/bash

restart_all: stop start

stop:
	docker-compose -f ~/parkun-bot/env_parkun/docker-compose-prod-env.yml -f ~/parkun-bot/env_parkun/docker-compose-bot.yml down
	docker-compose -f ~/appeal_sender/docker-compose.yml down

start:
	docker-compose -f ~/parkun-bot/env_parkun/docker-compose-prod-env.yml -f ~/parkun-bot/env_parkun/docker-compose-bot.yml up -d --build
	sleep 5
	docker-compose -f ~/appeal_sender/docker-compose.yml up -d --build
