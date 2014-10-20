"""Test scaffold's session handling
"""
# third-party imports
import webapp2

# local imports
from app import config
from app.base import handlers
from tests.testcases import BaseTestCase


# test fixtures: we need to set up a local wsgi app so we can test the login
# decorators against real handlers


class SetHandler(handlers.BaseHandler):
  """Convenience class to verify successful requests."""

  def get(self):
    self.session['test'] = 'just testing'
    self._RawWrite('success')


class GetHandler(SetHandler):

    def get(self):
        self._RawWrite(self.session.get('test', 'no sell :('))


wsgi = webapp2.WSGIApplication([('/get', GetHandler), ('/set', SetHandler)], config=config.CONFIG)


class SessionHandlingTests(BaseTestCase):

    def test_setting_session_var_and_retrieve_on_next_request(self):
        """Test persisting a session variable and reading it back
        """

        response = wsgi.get_response('/set')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)

        # Can do the same for data, allowing you to store it as a map.
        headers = [('Cookie', response.headers['Set-Cookie'])]

        response = wsgi.get_response('/get', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('just testing', response.body)
