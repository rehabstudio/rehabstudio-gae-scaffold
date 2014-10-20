"""Application configuration"""
# third-party imports
import webapp2
from google.appengine.api import users

# local imports
from .base import constants
from .base import models


# Place global application configuration settings (e.g. settings for
# 'webapp2_extras.sessions') here.
#
# These values will be accessible from handler methods like this:
# self.app.config.get('foo')
#
# Framework level settings:
#
#   using_angular:  True or False (default).  When True, an XSRF-TOKEN cookie
#                   will be set for interception/use by Angular's $http service.
#                   When False, no header will be set (but an XSRF token will
#                   still be available under the _xsrf key for Jinja templates).
#                   If you set this to True, be especially careful
#                   when mixing Angular and Jinja2 templates:
#                   https://github.com/angular/angular.js/issues/5601. See the
#                   summary by IgorMinar for details.
#
#   framing_policy: one of base.constants.DENY (default),
#                   base.constants.SAMEORIGIN, or base.constants.PERMIT
#
#   hsts_policy:    A dictionary with minimally a 'max_age' key, and optionally
#                   a 'includeSubdomains' boolean member.
#                   Default: { 'max_age': 2592000, 'includeSubDomains': True }
#                   implying 30 days of strict HTTPS for all subdomains.
#
#   csp_policy:     A dictionary with keys that correspond to valid CSP
#                   directives, as defined in the W3C CSP 1.1 spec.  Each
#                   key/value pair is transmitted as a distinct
#                   Content-Security-Policy header.
#                   Default: {'default-src': '\'self\''}
#                   which is a very restrictive policy.  An optional
#                   'reportOnly' boolean key substitutes a
#                   'Content-Security-Policy-Report-Only' header
#                   name in lieu of 'Content-Security-Policy' (the default
#                   is base.constants.DEBUG).
#
#  Note that the default values are also configured in app.yaml for files
#  served via the /static/ resources.  You may need to change the settings
#  there as well.

try:
    session_key = models.GetApplicationConfiguration().session_key
except AssertionError:
    # catch assertion error thrown when we import this module during test
    # runs. normally we'd use the appengine testbed to register the stubs, but
    # this particular import happens up front and so we haven't initiated the
    # testbed when it's imported.
    session_key = 'testingkey'

CONFIG = {
    # Developers are encouraged to build sites that comply with this (or
    # a similarly restrictive) CSP policy.  In particular, adding directives
    # such as unsafe-inline or unsafe-eval is highly discouraged, as these
    # may lead to XSS attacks.
    'csp_policy': {
        'font-src':    '\'self\'',
        'frame-src':   '\'self\'',
        'script-src':  '\'self\'',
        'style-src':   '\'self\'',
        'img-src':     '\'self\'',
        # fallback
        'default-src': '\'self\'',
        'report-uri':  '/csp',
        'reportOnly': constants.DEBUG,
    },
    # Configure global context/filters/settings for Jinja2
    'jinja2': {
        'globals': {
            'uri_for': webapp2.uri_for,
            'logout_url': users.create_logout_url,
        },
        'filters': {},
    },
    'webapp2_extras.sessions': {
        'secret_key': session_key,
    },
}
