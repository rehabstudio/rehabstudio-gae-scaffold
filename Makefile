COMPOSE = docker-compose -f ./ops/docker-compose.yml
SERVER = backend
CLIENT = frontend

CONTAINER = $(SERVER)


# Make the deploy target configurable on the command line
# user can pass `app=<appname>` or `version=<version>` to control where the
# app gets deployed
app ?= gae-secure-scaffold
version ?= development


help:
	@echo "$(app)"
	@echo ""
	@echo "The following commands are available:"
	@echo ""
	@echo "    make deploy:  Deploy the application to the specified appengine instance."
	@echo "                  Accepts args: app, version (see Makefile comments)"
	@echo "    make run:     Run local development server"
	@echo "    make test:    Run application's tests"

run:
	$(COMPOSE) up

shell:
	$(COMPOSE) run $(CONTAINER) bash

test:
	$(COMPOSE) run $(CONTAINER) make test

build:
	$(COMPOSE) run $(CLIENT) make build

watch:
	$(COMPOSE) run $(CLIENT) make watch


# Ensures that no untracked/uncommitted files are present in the repository
dirtycheck:
	@python ./ops/dirtycheck.py . --quiet || (echo "Git repository is dirty: Please commit your changes."; exit 1)
	@echo "Git repository is clean: Continuing."


# Deploy the application to the live appengine environment. Deployment is only
# possible if the repository is clean, you cannot deploy uncommitted code into
# a prouction environment. dev, staging or live, there's no difference, don't
# deploy untrackable code. This target accepts the following arguments:
#
#     app=<app_name>
#     		application id to which to deploy
#     		e.g. `app=someapp` would deploy to someapp.appspot.com
#
#     version=<version_id>: sub-version that should be used for deployment

deploy: dirtycheck build
	$(COMPOSE) run $(SERVER) make deploy app=$(app) version=$(version)


# special command to change target container to the client so we run commands
# like `make client shell`
client:
	-$(eval CONTAINER := $(CLIENT))


.PHONY: deploy client run shell test build watch dirtycheck help
