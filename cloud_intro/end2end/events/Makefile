#!/usr/bin/make -f

ROOT_FOLDER := $(shell pwd)

launch-events-brokers-mac:
	@HOST_IP=$(shell ipconfig getifaddr en0) docker-compose up

launch-events-brokers-ubuntu:
	@HOST_IP=$(shell ip -o -4 addr show wlan0 | awk '{print $$4}' | cut -d/ -f1) docker-compose up

stop-events-brokers:
	docker-compose down