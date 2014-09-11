# These variables are used throughout the makefile to provide unique
# per-project containers and images.
CID = $(shell python ops/scripts/cidgen.py)
IMGNM = gae_scaffold/$(CID)
STRGCNTNR = $(CID)-storage
RNCNTNR = $(CID)-run

# Make the deploy target configurable on the command line
# user can pass `app=<appname>` or `version=<version>` to control where the
# app gets deployed
ifndef app
	app = gae-scaffold
endif
ifndef version
	version = development
endif

# If running on Linux (and thus using docker directly) we set can use the
# created user (as specified in the Dockerfile). If running on Mac (and thus
# on top of boot2docker) we need to use root since Virtualbox takes care of
# ensuring any created files have the correct permissions and will complain if
# a non-root user is used inside the container for certain things (like `npm
# install`).
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
	USE_ROOT =
else ifeq ($(UNAME), Darwin)
	USE_ROOT = -u 0
endif

help:
	@echo "deploy: Deploy the application to the configured appengine account/version."
	@echo "run:    Run development server inside a Docker container."
	@echo "shell:  Open a Bash shell inside the container environment."
	@echo "test:   Run application's tests inside a docker container."

build:
	docker build -t="$(IMGNM)" .

dirtycheck:
	@python ./ops/scripts/dirtycheck.py . --quiet || (echo "Git repository is dirty: Please commit your changes."; exit 1)
	@echo "Git repository is clean: Continuing."

deploy: dirtycheck storage
	docker run -t -i --volumes-from $(STRGCNTNR) -v $(CURDIR)/app:/app $(USE_ROOT) $(IMGNM) make -C /app deploy app=$(app) version=$(version)

pyshell: storage
	docker run -t -i --rm --volumes-from $(STRGCNTNR) -v $(CURDIR)/app:/app $(USE_ROOT) $(IMGNM) remote_shell.py

storage: build
	-docker run -t -i --name $(STRGCNTNR) -u 0 $(IMGNM) bootstrap_storage.sh

run: storage
	@-docker kill $(RNCNTNR)
	@-docker rm $(RNCNTNR)
	docker run -t -i --rm --name $(RNCNTNR) --volumes-from $(STRGCNTNR) -v $(CURDIR)/app:/app -p 0.0.0.0:8080:8080 -p 0.0.0.0:8000:8000 $(USE_ROOT) $(IMGNM) make -C /app run

shell: storage
	docker run -t -i --volumes-from $(STRGCNTNR) -v $(CURDIR)/app:/app -v $(CURDIR)/output:/output $(USE_ROOT) $(IMGNM) bash

test: build
	docker run -t -i -v $(CURDIR)/app:/app -v $(CURDIR)/output:/output $(USE_ROOT) $(IMGNM) make -C /app test
