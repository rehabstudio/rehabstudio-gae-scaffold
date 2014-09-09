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
"""Main application entry point.
"""
# do some monkey patching
from .base import api_fixer

# third-party imports
import webapp2

# local imports
from . import config
from . import routes
from .base import constants


#################################
# DO NOT MODIFY BELOW THIS LINE #
#################################

app = webapp2.WSGIApplication(
    routes=(routes.ROUTES),
    debug=constants.DEBUG,
    config=config.CONFIG)
