#!/bin/sh
set -e

while true; do
    inotifywait -r -e modify --exclude="(.swp|.pyc)" .
    make test
done
