"""Route/URL definitions for the app"""
# stdlib imports
import itertools

# third-party imports
from webapp2 import Route

# local imports
from . import handlers


# These should all inherit from base.handlers.BaseHandler
_UNAUTHENTICATED_ROUTES = [('/', handlers.RootHandler),
                           ('/xss', handlers.XssHandler),
                           ('/xssi', handlers.XssiHandler),
                           Route(r'/oauth/start-login/', 'app.oauth.handlers.StartLoginHandler', name='oauth-start-login'),
                           Route(r'/oauth/handle-callback/', 'app.oauth.handlers.HandleCallbackHandler', name='oauth-handle-callback'),
                           Route(r'/oauth/logout/', 'app.oauth.handlers.LogoutHandler', name='oauth-logout')]

# These should all inherit from base.handlers.BaseAjaxHandler
_UNAUTHENTICATED_AJAX_ROUTES = [('/csp', handlers.CspHandler)]

# These should all inherit from base.handlers.AuthenticatedHandler
_USER_ROUTES = [('/xsrf', handlers.XsrfHandler), ('/oxsrf', handlers.OAuthXsrfHandler)]

# These should all inherit from base.handlers.AuthenticatedAjaxHandler
_AJAX_ROUTES = []

# These should all inherit from base.handlers.AdminHandler
_ADMIN_ROUTES = []

# These should all inherit from base.handlers.AdminAjaxHandler
_ADMIN_AJAX_ROUTES = []

# These should all inherit from base.handlers.BaseCronHandler
_CRON_ROUTES = []

# These should all inherit from base.handlers.BaseTaskHandler
_TASK_ROUTES = []


# Aggregate all the routes into something we can pass directly to our WSGI app
ROUTES = list(itertools.chain(
    _UNAUTHENTICATED_ROUTES,
    _UNAUTHENTICATED_AJAX_ROUTES,
    _USER_ROUTES,
    _AJAX_ROUTES,
    _ADMIN_ROUTES,
    _ADMIN_AJAX_ROUTES,
    _CRON_ROUTES,
    _TASK_ROUTES,
))
