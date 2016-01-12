"""Test scaffold's session handling
"""
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


# test fixtures: we need to set up a local wsgi app so we can test the login
# decorators against real handlers


class SetHandler(handlers.AuthenticatedHandler):
    """Convenience class to verify successful requests."""

    def get(self):
        self.session['test'] = 'success'
        self._RawWrite('success')

    def DenyAccess(self):
        self.session['test'] = 'access_denied'
        self._RawWrite('access_denied')

    def XsrfFail(self):
        self.session['test'] = 'xsrf_fail'
        self._RawWrite('xsrf_fail')


class GetHandler(SetHandler):

    def get(self):
        self._RawWrite(self.session.get('test', 'no sell :('))


class RaiseHandler(GetHandler):

    def DenyAccess(self):
        self.session['test'] = 'exc_access_denied'
        webapp2.abort(401)


wsgi = webapp2.WSGIApplication([('/get', GetHandler), ('/set', SetHandler), ('/raise', RaiseHandler)], config=config.CONFIG)


class SessionHandlingTests(BaseTestCase):

    def test_setting_session_var_and_retrieve_on_next_request(self):
        """Test persisting a session variable and reading it back
        """

        self._FakeLogin()

        response = wsgi.get_response('/set')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)

        headers = [('Cookie', response.headers['Set-Cookie'])]

        response = wsgi.get_response('/get', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)

    def test_setting_session_var_and_retrieve_on_next_request_with_access_denied(self):
        """Test persisting a session variable and reading it back when access is denied
        """

        response = wsgi.get_response('/set')
        self.assertEqual(200, response.status_int)
        self.assertEqual('access_denied', response.body)

        headers = [('Cookie', response.headers['Set-Cookie'])]

        self._FakeLogin()

        response = wsgi.get_response('/get', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('access_denied', response.body)

    def test_setting_session_var_and_retrieve_on_next_request_with_xsrf_fail(self):
        """Test persisting a session variable and reading it back when there is an XSRF failure
        """

        self._FakeLogin()

        response = _make_test_request(wsgi, '/set', method='POST')
        self.assertEqual(200, response.status_int)
        self.assertEqual('xsrf_fail', response.body)

        headers = [('Cookie', response.headers['Set-Cookie'])]

        response = wsgi.get_response('/get', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('xsrf_fail', response.body)

    def test_setting_session_var_and_retrieve_on_next_request_with_exc_during_access_denied(self):
        """Test persisting a session variable and reading it back when an exception is thrown in DenyAccess
        """

        response = wsgi.get_response('/raise')
        self.assertEqual(401, response.status_int)

        headers = [('Cookie', response.headers['Set-Cookie'])]

        self._FakeLogin()

        response = wsgi.get_response('/get', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('exc_access_denied', response.body)
