SHELL := /bin/bash

reboot: stop start

stop:
	docker-compose -f ~/parkun-bot/env_parkun/docker-compose-bot.yml down
	docker-compose -f ~/parkun-bot/env_parkun/docker-compose-prod-env.yml down
	-pkill -f main.py
	-pkill -f chrom

start:
	docker-compose -f ~/parkun-bot/env_parkun/docker-compose-prod-env.yml up -d --build
	docker-compose -f ~/parkun-bot/env_parkun/docker-compose-bot.yml up -d --build
	sleep 10
	source ~/appeal_sender/.venv/bin/activate; \
	(nohup python ~/appeal_sender/main.py &> ~/appeal_sender/log.txt < /dev/null &) && /bin/true
