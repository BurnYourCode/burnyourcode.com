.PHONY: build run deploy synconly

build:
	rm -rf _build
	python3 genox.py

run:
	python3 server.py _build

deploy: build
	cd deployment && \
		ansible-playbook -l live -i hosts deploy.yml --ask-become-pass

synconly: build
	cd deployment && \
		ansible-playbook -l live -i hosts deploy.yml --tags=synconly
