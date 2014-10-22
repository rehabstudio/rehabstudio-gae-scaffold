"""Backends for webapp2 OAuth support
"""
# future imports
from __future__ import absolute_import

# stdlib imports
import json
import logging
import sys
import urllib
import uuid

# third-party imports
import webapp2
from google.appengine.api import urlfetch

# local imports
from app.utils.network import make_request


class OAuthUser(object):
    """Dummy user object used when a user has logged in via Oauth
    """

    def __init__(self, user_data):
        self.user_data = user_data

    def email(self):
        return self.user_data['emails'][0]['value']

    def user_id(self):
        return self.user_data['id']


class BackendConfigurationError(Exception):
    pass


def get_backend(backend_name, config, session, request):
    """Returns an instantiated OAuth2 backend

    If a valid backend is not available `None` is returned. If a valid backend
    is available but the required configuration values have not been set, a
    warning message is logged (with instructions on what configuration needs
    set) and None is still returned. This allows backends to be
    enabled/disabled via configuration file.
    """
    # get backend class from current module if one exists
    backend_name = backend_name.lower().capitalize() + 'Backend'
    backend = getattr(sys.modules[__name__], backend_name)
    if backend is None:
        return None
    # initialise class and check configuration
    try:
        return backend(config, session, request)
    # log error message if not configured properly
    except BackendConfigurationError:
        logging.warning('Backend not configured: {0}'.format(backend_name))
        for req_conf in backend.required_configuration_values:
            logging.warning('{0} is a required setting'.format(req_conf))
        return None
    # catch if someone tries to be clever with the url and use the base backend directly
    except NotImplementedError:
        logging.warning('Cannot use the base backend directly')
        return None


class BaseBackend(object):

    required_configuration_values = []

    def __init__(self, config, session, request):
        self.config = config
        self.session = session
        self.request = request
        self.load_configuration()

    @property
    def next_url(self):
        """Grab the redirect URL from the user's session.
        """
        try:
            url = self.session.pop('next_url')
        except KeyError:
            url = '/'
        return url

    def load_configuration(self):
        for rc in self.required_configuration_values:
            conf_value = self.config.get(rc, None)
            if conf_value is None:
                raise BackendConfigurationError(rc)
            setattr(self, rc, conf_value)


class GoogleBackend(BaseBackend):

    required_configuration_values = [
        'google_oauth_client_id',
        'google_oauth_client_secret',
        'google_oauth_scopes',
    ]

    def start_login(self):
        """Called when a user initiates login

        Returns a URL to which the user should be redirected for login.
        """
        params = {
            'scope': ' '.join(self.google_oauth_scopes),
            'redirect_uri': webapp2.uri_for('oauth-handle-callback', _full=True),
            'response_type': 'code',
            'client_id': self.google_oauth_client_id,
            'state': str(uuid.uuid4()),
            "access_type": "offline",
            "approval_prompt": "auto",
        }
        self.session.update({'GOOGLE_OAUTH_STATE': params['state']})
        return 'https://accounts.google.com/o/oauth2/auth?' + urllib.urlencode(params)

    def handle_callback(self):
        """Handles an oauth callback
        """
        # ensure callback is valid and user has granted authorisation
        try:
            csrf = self.session.pop('GOOGLE_OAUTH_STATE') == self.request.GET['state']
        except KeyError:
            webapp2.abort(401, detail="CSRF/state missing")
        if not csrf or 'error' in self.request.GET:
            webapp2.abort(401, detail="CSRF/state mismatch")

        # exchanges code received from Google for an access token
        params = {
            'code': self.request.GET['code'],
            'client_id': self.google_oauth_client_id,
            'client_secret': self.google_oauth_client_secret,
            'redirect_uri': self.request.path_url,
            'grant_type': 'authorization_code',
        }
        _url = 'https://accounts.google.com/o/oauth2/token'
        resp = make_request(_url, payload=urllib.urlencode(params), method=urlfetch.POST)
        token_data = json.loads(resp.content)

        # save token and user data in the user's session
        self.session.update({
            'TOKEN_DATA': token_data,
            'USER_DATA': self.get_user_data(token_data['access_token'])
        })

        # get a valid redirect URL from the session, falling back to the
        # application root if no URL is stored in the session
        return self.next_url

    def logout(self):
        """Flush OAuth related data from the session and return a URL to
        redirect the user to.
        """
        try:
            del self.session['TOKEN_DATA']
        except KeyError:
            pass
        try:
            del self.session['USER_DATA']
        except KeyError:
            pass
        return self.next_url

    def get_user_data(self, oauth_token):
        """Fetch user data from the G+ API
        """
        _url = 'https://www.googleapis.com/plus/v1/people/me'
        _headers = {'Authorization': 'Bearer {0}'.format(oauth_token)}
        user_data = json.loads(make_request(_url, headers=_headers).content)
        if 'error' in user_data:
            webapp2.abort(401)
        return user_data
