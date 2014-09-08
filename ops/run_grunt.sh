#!/bin/bash
set -e

cd /app/
npm install
grunt clean
grunt
grunt appengine:run:app
