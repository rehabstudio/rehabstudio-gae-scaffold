"""Route/URL definitions for the app"""
# stdlib imports
import itertools

# local imports
from . import handlers
from .examples import example_handlers


# These should all inherit from base.handlers.BaseHandler
_UNAUTHENTICATED_ROUTES = [('/', handlers.RootHandler),
                           ('/examples/xss',
                            example_handlers.ClosureXssHandler),
                           ('/examples/jinja',
                            example_handlers.JinjaXssHandler),
                           ('/examples/csp', example_handlers.CspHandler),
                           ('/examples/xssi', example_handlers.XssiHandler)]

# These should all inherit from base.handlers.BaseAjaxHandler
_UNAUTHENTICATED_AJAX_ROUTES = [('/csp', handlers.CspHandler)]

# These should all inherit from base.handlers.AuthenticatedHandler
_USER_ROUTES = [('/examples/xsrf', example_handlers.XsrfHandler)]

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
