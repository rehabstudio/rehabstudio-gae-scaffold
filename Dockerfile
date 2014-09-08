FROM debian:wheezy
MAINTAINER Paddy Carey <patrick@rehabstudio.com>

# empty file that when touched will force a full rebuild of the container
ADD ops/force_rebuild /force_rebuild

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing && apt-get upgrade -y

# install packages from apt
RUN apt-get install -y ca-certificates apt-transport-https make wget unzip python-pip python-imaging python-numpy

# install packages from PyPI
ADD ops/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Download and install the Appengine Python SDK
RUN wget -nv https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.10.zip && \
    unzip -q google_appengine_1.9.10.zip && rm google_appengine_1.9.10.zip
ENV PATH /google_appengine:$PATH

# use a volume to persist application data across container restarts
VOLUME ["/.appengine_storage"]

# Download and install node.js
ADD ops/nodesource.list /etc/apt/sources.list.d/nodesource.list
RUN wget -nv https://deb.nodesource.com/gpgkey/nodesource.gpg.key && \
    apt-key add nodesource.gpg.key && rm nodesource.gpg.key && \
    apt-get update && apt-get install -y nodejs && npm install -g grunt-cli

# copy the grunt run script into place and give it the right permissions
ADD ops/run_grunt.sh /usr/local/bin/run_grunt.sh
RUN chmod a+x /usr/local/bin/run_grunt.sh

# default run command
CMD bash

# expose ports (application server & admin server)
EXPOSE 8080
EXPOSE 8000
