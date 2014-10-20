FROM debian:wheezy
MAINTAINER Paddy Carey <patrick@rehabstudio.com>

# empty file that when touched will force a full rebuild of the container
ADD ops/force_rebuild /force_rebuild

# no tty
ENV DEBIAN_FRONTEND noninteractive

# update apt cache, upgrade the system and install the system utils we need
RUN apt-get update --fix-missing && \
    apt-get upgrade -y && \
    apt-get install -y apt-transport-https

# Add GPG key and repo definition that will allow us to install nodejs
ADD ops/nodejs/nodesource.list /etc/apt/sources.list.d/nodesource.list
ADD ops/nodejs/nodesource.gpg.key /tmp/nodesource.gpg.key
RUN apt-key add /tmp/nodesource.gpg.key && \
    apt-get update

# install packages from apt
RUN apt-get install -y inotify-tools make nodejs python-imaging python-numpy python-pip sudo unzip wget

# install system-wide packages from PyPI
ADD ops/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# install system-wide packages from npm
RUN npm install -g grunt-cli gulp

# Download and install the Appengine Python SDK
RUN cd /opt/ && \
    wget -nv https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.13.zip && \
    unzip -q google_appengine_1.9.13.zip && \
    rm google_appengine_1.9.13.zip
ENV PATH /opt/google_appengine:$PATH

# Add the remote_shell.py script to the $PATH and make it executable
ADD ops/scripts/remote_shell.py /usr/local/bin/remote_shell.py
RUN chmod a+x /usr/local/bin/remote_shell.py

# use volumes to persist application data across container restarts
VOLUME ["/.appengine_storage"]
VOLUME ["/.ipython"]
VOLUME ["/home/aeuser"]

# create a non-root user we can use to run the application inside the container
RUN groupadd -r aeuser -g 1000 && \
    useradd -u 1000 -r -g aeuser -d /home/aeuser -s /bin/bash -c "Docker/GAE image user" aeuser

# Add the bootstrap_storage.sh script to the $PATH and make it executable
ADD ops/scripts/bootstrap_storage.sh /usr/local/bin/bootstrap_storage.sh
RUN chmod a+x /usr/local/bin/bootstrap_storage.sh

# Add the watch.sh script to the $PATH and make it executable
ADD ops/scripts/watch.sh /usr/local/bin/watch.sh
RUN chmod a+x /usr/local/bin/watch.sh

# add .bashrc to ~/
ADD ops/shell/bashrc /home/aeuser/.bashrc

# add a custom motd to remind users of how persistance works in the container
ADD ops/shell/motd /etc/motd

# Add custom sudo config to enable root access for aeuser
ADD ops/shell/sudoers /etc/sudoers.d/aeuser

# switch to the new user account so that all commands run as `aeuser` by default
ENV HOME /home/aeuser
USER aeuser

# default run command
CMD bash

# expose ports (application server & admin server)
EXPOSE 8080
EXPOSE 8000
