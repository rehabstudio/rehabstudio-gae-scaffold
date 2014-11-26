FROM debian:wheezy
MAINTAINER Paddy Carey <patrick@rehabstudio.com>

# update apt cache, upgrade the system and install the system utils we need
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-transport-https

# copy all necessary assets and scripts into the container, put them in the
# right places and ensure the correct permissions are set.
COPY ops/ /ops/
RUN bash /ops/install_assets_and_scripts.sh

# Add GPG key and repo definition that will allow us to install nodejs and update
# the apt-cache again
RUN apt-key add /ops/assets/nodesource.gpg.key && apt-get update

# install all the packages we need from apt, pypi and npm
RUN apt-get install -y inotify-tools make nodejs python-imaging python-numpy python-pip sudo && \
    pip install -r /ops/assets/requirements.txt && \
    npm install -g grunt-cli gulp

# Download and install the Appengine Python SDK
RUN python /ops/scripts/gaesdk_download.py 1.9.15
ENV PATH /opt/google_appengine:$PATH

# use volumes to persist application data across container restarts
VOLUME ["/.appengine_storage", "/.ipython", "/home/aeuser"]

# create a non-root user we can use to run the application inside the container
RUN groupadd -r aeuser -g 1000 && \
    useradd -u 1000 -r -g aeuser -d /home/aeuser -s /bin/bash -c "Docker/GAE image user" aeuser

# switch to the new user account so that all commands run as `aeuser` by default
ENV HOME /home/aeuser
USER aeuser

# default run command
CMD bash

# expose ports (application server & admin server)
EXPOSE 8000 8080
