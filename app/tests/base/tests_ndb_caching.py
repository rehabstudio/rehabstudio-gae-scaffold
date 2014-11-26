"""Tests for ndb caching behaviour.

This test is for a bug first reported at
https://github.com/rehabstudio/rehabstudio-gae-scaffold/issues/3 wherein
during test runs the ndb in-context cache doesn't seem to be clearing as it
should.
"""
# third-party imports
from google.appengine.ext import ndb

# local imports
from tests.testcases import BaseTestCase


# This import (unused in this particular test case) is found in many
# of the test modules already present in app/tests/base. It appears
# that the call to GetApplicationConfiguration within app/config.py
# causes the bug. Remove this import to see that the problem is
# resolved.
from app import config


class MyModel(ndb.Model):
    value = ndb.StringProperty()


class ExampleTestCase(BaseTestCase):

    def test_1_model_is_created(self):
        """ Persist an object in the datastore with and ID of 1234.
        """
        MyModel(id=1234, value='foobar').put()
        self.assertEqual(len(MyModel.query().fetch()), 1)

    def test_2_model_no_longer_exists(self):
        """ Assert that the datastore is reset from the previous test
        run and that object 1234 is no longer present in the datastore.
        """
        self.assertEqual(len(MyModel.query().fetch()), 0)
        self.assertIsNone(MyModel.get_by_id(1234))
