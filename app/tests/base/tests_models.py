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
"""Tests for base.models.
"""
# stdlib imports
import unittest

# third-party imports
from google.appengine.ext import testbed

# local imports
from app.base import models


class ModelsTest(unittest.TestCase):
  """Test cases for base.models."""

  def setUp(self):
    self.testbed = testbed.Testbed()
    self.testbed.activate()
    self.testbed.init_datastore_v3_stub()

  def testConfigurationAutomaticallyGenerated(self):
    config = models.GetApplicationConfiguration()
    self.assertIsNotNone(config)
    self.assertIsNotNone(config.xsrf_key)
