#!/bin/bash
set -e

# fix permissisons on mounted volumes
chown -R aeuser:aeuser /.appengine_storage
chown -R aeuser:aeuser /.ipython
chown -R aeuser:aeuser /home/aeuser

echo "Storage container bootstrapped."
