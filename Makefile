# The name of the project is used throughout the makefile to provide
# project-specific docker containers.
PROJNAME = rehabstudio-gae-scaffold

# If running on Linux (and thus using docker directly) we set the user id to
# that of the current user. If running on Mac (and thus on top of boot2docker)
# we don't bother since Virtualbox takes care of ensuring any created files
# have the correct permissions.
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
	USER_ID = -u $(shell id -u $$USER)
else ifeq ($(UNAME), Darwin)
	USER_ID =
endif


help:
	@echo "run - Run development server inside a Docker container"
	@echo "test - Run application's tests inside a docker container"

build:
	docker build -t="appengine/$(PROJNAME)" .

dirtycheck:
	@python ./ops/scripts/dirtycheck.py . --quiet || (echo "Git repository is dirty: Please review and try again."; exit 1)
	@echo "Git repository is clean: Continuing."

deploy: dirtycheck storage
	docker run -t -i --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app appengine/$(PROJNAME) make -C /app deploy

storage: build
	-docker run -t -i --name $(PROJNAME) appengine/$(PROJNAME) echo "Storage-only container."

run: storage
	docker run -t -i --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app -p 0.0.0.0:8080:8080 -p 0.0.0.0:8000:8000 appengine/$(PROJNAME) make -C /app run

shell: storage
	docker run -t -i --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app -p 0.0.0.0:8080:8080 -p 0.0.0.0:8000:8000 appengine/$(PROJNAME) bash

test: build
	docker run -t -i -v $(CURDIR)/app:/app -v $(CURDIR)/output:/output $(USER_ID) appengine/$(PROJNAME) make -C /app test
