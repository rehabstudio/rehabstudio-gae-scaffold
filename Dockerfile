FROM debian:wheezy
MAINTAINER Paddy Carey <patrick@rehabstudio.com>

# empty file that when touched will force a full rebuild of the container
ADD ops/force_rebuild /force_rebuild

# no tty
ENV DEBIAN_FRONTEND noninteractive

# update apt cache, upgrade the system and install the system utils we need
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y apt-transport-https ca-certificates make unzip wget

# Add GPG key and repo definition that will allow us to install nodejs
ADD ops/nodejs/nodesource.list /etc/apt/sources.list.d/nodesource.list
ADD ops/nodejs/nodesource.gpg.key /tmp/nodesource.gpg.key
RUN apt-key add /tmp/nodesource.gpg.key
RUN apt-get update

# install packages from apt
RUN apt-get install -y nodejs python-imaging python-numpy python-pip

# install system-wide packages from PyPI
ADD ops/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# install system-wide packages from npm
RUN npm install -g grunt-cli gulp

# Download and install the Appengine Python SDK
RUN cd /opt/ && wget -nv https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.10.zip
RUN cd /opt/ && unzip -q google_appengine_1.9.10.zip && rm google_appengine_1.9.10.zip
ENV PATH /opt/google_appengine:$PATH

# patch the SDK so we can bind the remote API server to something other than localhost
ADD ops/sdk_patches/appengine_rpc.py /opt/google_appengine/google/appengine/tools/appengine_rpc.py

# Add the remote_shell.py script to the $PATH and make it executable
ADD ops/scripts/remote_shell.py /usr/local/bin/remote_shell.py
RUN chmod a+x /usr/local/bin/remote_shell.py

# get the ip address of the host as exposed inside the container
RUN /sbin/ip route|awk '/default/ { print $3 }' > /etc/host_ip

# use a volume to persist application data across container restarts
VOLUME ["/.appengine_storage"]

# default run command
CMD bash

# expose ports (application server & admin server)
EXPOSE 8080
EXPOSE 8000
