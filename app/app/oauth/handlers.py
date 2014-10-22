# marty mcfly imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import abc

# third-party imports
import webapp2

# local imports
from . import backends
from app.base import constants
from app.base import handlers
from app.base import xsrf


class OAuthBackendHandler(handlers.BaseHandler):

    def get_backend(self):
        return backends.get_backend(
            'google',
            self.app.config,
            self.session,
            self.request
        )


class StartLoginHandler(OAuthBackendHandler):

    def get(self):
        backend = self.get_backend()
        if backend is None:
            return webapp2.abort(404)
        return self.redirect(backend.start_login())


class HandleCallbackHandler(OAuthBackendHandler):

    def get(self):
        backend = self.get_backend()
        if backend is None:
            return webapp2.abort(404)
        return self.redirect(backend.handle_callback())


class LogoutHandler(OAuthBackendHandler):

    def get(self):
        backend = self.get_backend()
        if backend is None:
            return webapp2.abort(404)
        return self.redirect(backend.logout())


class AuthenticatedHandler(handlers.BaseHandler):
    """Base handler for servicing authenticated user requests.

    Implementations should provide an implementation of DenyAccess()
    and XsrfFail() to handle unauthenticated requests or invalid XSRF tokens.

    POST requests will be rejected unless the request contains a
    parameter named 'xsrf' which is a valid XSRF token for the
    currently authenticated user.
    """

    __metaclass__ = handlers._HandlerMeta

    @handlers.requires_auth
    @handlers.xsrf_protected
    def dispatch(self):
        super(AuthenticatedHandler, self).dispatch()

    def _RequestContainsValidXsrfToken(self):
        token = self.request.get(
            'xsrf') or self.request.headers.get('X-XSRF-TOKEN')
        # By default, Angular's $http service will add quotes around the
        # X-XSRF-TOKEN.
        if (token and
                self.app.config.get('using_angular', constants.DEFAULT_ANGULAR) and
                token[0] == '"' and token[-1] == '"'):
            token = token[1:-1]

        if xsrf.ValidateToken(handlers._GetXsrfKey(), self.current_user.email(),
                              token):
            return True
        return False

    @webapp2.cached_property
    def current_user(self):
        # grab user data from session
        try:
            user_data = self.session['USER_DATA']
        except KeyError:
            return None
        return backends.OAuthUser(user_data)

    @abc.abstractmethod
    def DenyAccess(self):
        pass

    @abc.abstractmethod
    def XsrfFail(self):
        pass


class AuthenticatedAjaxHandler(handlers.BaseAjaxHandler):
    """Base handler for servicing AJAX requests.

    Implementations should provide an implementation of DenyAccess()
    and XsrfFail() to handle unauthenticated requests or invalid XSRF tokens.

    POST requests will be rejected unless the request contains a
    parameter named 'xsrf', OR an HTTP header named 'X-XSRF-Token'
    which is a valid XSRF token for the currently authenticated user.

    Responses to GET requests will be prefixed by _XSSI_PREFIX.  Requests
    using other HTTP verbs will not include such a prefix.
    """

    __metaclass__ = handlers._HandlerMeta

    @handlers.requires_auth
    @handlers.xsrf_protected
    def dispatch(self):
        super(AuthenticatedAjaxHandler, self).dispatch()

    def _RequestContainsValidXsrfToken(self):
        token = self.request.get(
            'xsrf') or self.request.headers.get('X-XSRF-Token')
        # By default, Angular's $http service will add quotes around the
        # X-XSRF-TOKEN.
        if (token and
                self.app.config.get('using_angular', constants.DEFAULT_ANGULAR) and
                token[0] == '"' and token[-1] == '"'):
            token = token[1:-1]

        if xsrf.ValidateToken(handlers._GetXsrfKey(), self.current_user.email(),
                              token):
            return True
        return False

    @webapp2.cached_property
    def current_user(self):
        # grab user data from session
        try:
            user_data = self.session['USER_DATA']
        except KeyError:
            return None
        return backends.OAuthUser(user_data)

    def DenyAccess(self):
        webapp2.abort(401)

    @abc.abstractmethod
    def XsrfFail(self):
        webapp2.abort(400, detail="XSRF fail")
