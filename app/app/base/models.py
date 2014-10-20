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
"""Framework wide datastore models.
"""
# stdlib imports
import os

# third-party imports
from google.appengine.ext import ndb


@ndb.transactional
def GetApplicationConfiguration():
    """Returns the application configuration, creating it if necessary."""
    key = ndb.Key(Config, 'appconfig')
    entity = key.get()
    if not entity:
        entity = Config(key=key)
        entity.session_key = os.urandom(16)
        entity.xsrf_key = os.urandom(16)
        entity.put()
    return entity


class Config(ndb.Model):
    """A simple key-value store for application configuration settings."""

    session_key = ndb.BlobProperty()
    xsrf_key = ndb.BlobProperty()
