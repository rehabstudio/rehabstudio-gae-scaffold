# These variables are used throughout the makefile to provide unique
# per-project containers and images.
CID = $(shell python ops/scripts/cidgen.py)
IMAGE_NAME = gae_scaffold/$(CID)
STORAGE_CONTAINER = $(CID)-storage

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

# Base docker run command with common parameters
RUN_DOCKER = docker run -t -i --rm --net host --volumes-from $(STORAGE_CONTAINER) -v "$(CURDIR)/src:/src" -v "$(CURDIR)/output:/output"


# Show command line help message
help:
	@echo "gae-scaffold"
	@echo ""
	@echo "The following commands are available:"
	@echo ""
	@echo "    make deploy:  Deploy the application to the specified appengine instance."
	@echo "                  Accepts args: app, version (see Makefile comments)"
	@echo "    make run:     Run local development server inside container."
	@echo "    make test:    Run application's tests inside  container."
	@echo "    make shell:   Launch a Bash shell inside container."
	@echo "    make pyshell: Launch an IPython shell inside container."


# Builds the docker container that is run by our other targets
build:
	docker build -t="$(IMAGE_NAME)" .

# Used to provide a persistent container in which we can store semi-permanent
# but not critically important data i.e. deploy credentials, local databases,
# shell history etc.
storage: build
	-docker run -t -i --name $(STORAGE_CONTAINER) -u 0 $(IMAGE_NAME) bootstrap_storage.sh

# Ensures that no untracked/uncommitted files are present in the repository
dirtycheck:
	@python ./ops/scripts/dirtycheck.py . --quiet || (echo "Git repository is dirty: Please commit your changes."; exit 1)
	@echo "Git repository is clean: Continuing."


# Deploy the application to the live appengine environment. Deployment is only
# possible if the repository is clean, you cannot deploy uncommitted code into
# a prouction environment. dev, staging or live, there's no difference, don't
# deploy untrackable code. This target accepts the following arguments:
#
#     app=<app_name>:       application id to deploy to e.g. `app=someapp` would deploy to someapp.appspot.com
#     version=<version_id>: sub-version that should be used for deployment
deploy: dirtycheck storage
	$(RUN_DOCKER) $(USE_ROOT) $(IMAGE_NAME) make -C /src deploy app=$(app) version=$(version)

# Runs the application locally using the Appengine SDK. Your application code
# is mounted inside the docker container and the appropriate ports are bound
# to the host's network interface so it is possible to access the running
# server just as you usually would at http://localhost:8080 and the admin
# server on http://localhost:8000
run: storage
	$(RUN_DOCKER) -p 0.0.0.0:8080:8080 -p 0.0.0.0:8000:8000 --name gaerun-$(CID) $(USE_ROOT) $(IMAGE_NAME) make -C /src run

# Runs the application's tests using the appropriate test runners for each
# part of the application. All artifacts produced are saved to the `output/`
# directory on the host so they can be accessed outside the container e.g. by
# Jenkins.
test: storage
	$(RUN_DOCKER) $(USE_ROOT) $(IMAGE_NAME) make -C /src test


# Runs the application's tests continuously, watching for changes in the
# source files.
test-watch: storage
	$(RUN_DOCKER) $(USE_ROOT) $(IMAGE_NAME) make -C /src test-watch


# Launches a Bash shell inside the container environment for development
# purposes
shell: storage
	$(RUN_DOCKER) $(USE_ROOT) $(IMAGE_NAME) bash

# Launches an IPython shell and uses appengine's remote API functionality to
# allow the user to interact with live services from with the terminal/shell
# environment e.g. datastore, memcache, etc. Note: This target requires that
# you are already running a local server in another container.
pyshell: storage
	$(RUN_DOCKER) $(USE_ROOT) $(IMAGE_NAME) remote_shell.py


# Force stops the docker container (useful if the Appengine SDK hangs at
# shutdown, which it *loves* to do).
force-stop:
	docker stop gaerun-$(CID)
