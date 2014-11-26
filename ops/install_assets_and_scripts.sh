#!/bin/bash
set -e

# sources.list so we can install the latest node.js from apt
cp /ops/assets/nodesource.list /etc/apt/sources.list.d/nodesource.list

# Add the remote_shell.py script to the $PATH and make it executable
cp /ops/scripts/remote_shell.py /usr/local/bin/remote_shell.py
chmod a+x /usr/local/bin/remote_shell.py

# Add the bootstrap_storage.sh script to the $PATH and make it executable
cp /ops/scripts/bootstrap_storage.sh /usr/local/bin/bootstrap_storage.sh
chmod a+x /usr/local/bin/bootstrap_storage.sh

# Add the watch.sh script to the $PATH and make it executable
cp /ops/scripts/watch.sh /usr/local/bin/watch.sh
chmod a+x /usr/local/bin/watch.sh

# add .bashrc to ~/
mkdir -p /home/aeuser
cp /ops/assets/bashrc /home/aeuser/.bashrc

# add a custom motd to remind users of how persistance works in the container
cp /ops/assets/motd /etc/motd

# Add custom sudo config to enable root access for aeuser
mkdir -p /etc/sudoers.d
cp /ops/assets/sudoers /etc/sudoers.d/aeuser
