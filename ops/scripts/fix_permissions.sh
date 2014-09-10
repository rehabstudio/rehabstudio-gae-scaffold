#!/bin/bash
set -e

# fix permissisons on mounted volumes
chown -R aeuser:aeuser /.appengine_storage
chown -R aeuser:aeuser /.ipython

echo "Storage container created: Permissions fixed."
