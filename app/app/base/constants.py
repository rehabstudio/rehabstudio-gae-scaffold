# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
"""Public constants for use in application configuration.
"""
# stdlib imports
import os


def _IsDevAppServer():
    return os.environ.get('SERVER_SOFTWARE', 'Development').startswith('Development')

# webapp2 application configuration constants.

# using_angular
DEFAULT_ANGULAR = False

# framing_policy
(DENY, SAMEORIGIN, PERMIT) = range(0, 3)
X_FRAME_OPTIONS_VALUES = {DENY: 'DENY', SAMEORIGIN: 'SAMEORIGIN'}

# hsts_policy
DEFAULT_HSTS_POLICY = {'max_age': 2592000, 'includeSubdomains': True}

# csp_policy
DEFAULT_CSP_POLICY = {'default-src': '\'self\''}

# IS_DEV_APPSERVER is primarily used for decisions that rely on whether or
# not the application is currently serving over HTTPS (dev_appserver does
# not support HTTPS).
IS_DEV_APPSERVER = _IsDevAppServer()

DEBUG = IS_DEV_APPSERVER

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
