SHELL := /bin/bash

reboot: stop start

stop:
	docker-compose -f ~/parkun-bot/docker-compose.yml down
	-pkill -f main.py
	-pkill -f chrom

start:
	docker-compose -f ~/parkun-bot/docker-compose.yml up -d --build
	sleep 10
	source ~/appeal_preparer/.venv/bin/activate; \
	(nohup python ~/appeal_preparer/main.py &> ~/appeal_preparer/log.txt < /dev/null &) && /bin/true
