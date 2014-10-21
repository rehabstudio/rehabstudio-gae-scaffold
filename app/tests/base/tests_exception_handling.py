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
"""Tests for exception handling in AJAX handlers.
"""
# stdlib imports
import json

# third-party imports
import webapp2

# local imports
from app import config
from app.base import handlers
from tests.testcases import BaseTestCase


def _make_test_request(app, url, post_data=None, headers=None, method='GET'):
    """Make a test request against an app
    """
    request = webapp2.Request.blank(url, POST=post_data, headers=headers)
    request.method = method
    return request.get_response(app)


def strip_and_parse_as_json(json_string):
    """Strips the XSSI prefix from a JSON response and parses it into a python dict
    """
    json_string = json_string.replace(handlers._XSSI_PREFIX, '')
    return json.loads(json_string)


class AjaxHandler(handlers.BaseAjaxHandler):
    """Convenience class to verify exceptional requests."""

    def get(self):
        webapp2.abort(406)

    def post(self):
        raise AttributeError


class AuthedAjaxHandler(handlers.AuthenticatedAjaxHandler):
    """Convenience class to verify successful requests."""

    def get(self):
        webapp2.abort(406)

    def DenyAccess(self):
        webapp2.abort(407)

    def XsrfFail(self):
        webapp2.abort(408)


class HandlersTest(BaseTestCase):
    """Test cases for exception handling"""

    def setUp(self):
        self.app = webapp2.WSGIApplication([('/', AjaxHandler), ('/authed', AuthedAjaxHandler)], config=config.CONFIG)

    def testWebapp2ExceptionHandled(self):
        """Test that a webapp2.abort() is handled correctly within a JSON handler
        """

        response = self.app.get_response('/')
        self.assertEqual(406, response.status_int)
        self.assertEqual('406 Not Acceptable', strip_and_parse_as_json(response.body)['error'])

    def testGenericExceptionHandled(self):
        """Test that a generic exception is handled correctly within a JSON handler
        """

        response = _make_test_request(self.app, '/', method='POST')
        self.assertEqual(500, response.status_int)
        self.assertEqual('500 Server Error', strip_and_parse_as_json(response.body)['error'])

    def testWebapp2ExceptionHandledWhenAuthFails(self):
        """Test that a webapp2.abort() is handled correctly within an authed JSON handler when auth fails
        """

        response = self.app.get_response('/authed')
        self.assertEqual(407, response.status_int)
        self.assertEqual('407 Proxy Authentication Required', strip_and_parse_as_json(response.body)['error'])

    def testWebapp2ExceptionHandledWhenXsrfFails(self):
        """Test that a webapp2.abort() is handled correctly within an authed JSON handler when XSRF fails
        """

        self._FakeLogin()
        response = _make_test_request(self.app, '/authed', method='POST')
        self.assertEqual(408, response.status_int)
        self.assertEqual('408 Request Time-out', strip_and_parse_as_json(response.body)['error'])
