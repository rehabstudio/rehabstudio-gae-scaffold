# Copyright 2015 Google Inc. All rights reserved.
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
"""Tests for main."""

import webapp2
from webapp2 import import_string
from webapp2_extras.routes import MultiRoute

from app import routes
from app.base import handlers
from tests.testcases import BaseTestCase


class MainTest(BaseTestCase):

    """Test cases for main."""

    def _VerifyInheritance(self, routes_list, base_class):
        """Checks that the handlers of the given routes inherit from base_class."""

        router = webapp2.Router(routes_list)
        route_list = router.match_routes + router.build_routes.values()
        inheritance_errors = ''
        for route in route_list:
            if issubclass(route.__class__, MultiRoute):
                self._VerifyInheritance(list(route.get_routes()), base_class)
                continue

            # If the handler is in string from, request the the expected object
            if isinstance(route.handler, basestring):
                route.handler = import_string(route.handler)

            if issubclass(route.handler, webapp2.RedirectHandler):
                continue

            if not issubclass(route.handler, base_class):
                inheritance_errors += '* %s does not inherit from %s.\n' % (
                    route.handler.__name__, base_class.__name__)

        return inheritance_errors

    def testRoutesInheritance(self):
        errors = ''
        errors += self._VerifyInheritance(routes._UNAUTHENTICATED_ROUTES,
                                          handlers.BaseHandler)
        errors += self._VerifyInheritance(routes._UNAUTHENTICATED_AJAX_ROUTES,
                                          handlers.BaseAjaxHandler)
        errors += self._VerifyInheritance(routes._USER_ROUTES,
                                          handlers.AuthenticatedHandler)
        errors += self._VerifyInheritance(routes._AJAX_ROUTES,
                                          handlers.AuthenticatedAjaxHandler)
        errors += self._VerifyInheritance(routes._ADMIN_ROUTES,
                                          handlers.AdminHandler)
        errors += self._VerifyInheritance(routes._ADMIN_AJAX_ROUTES,
                                          handlers.AdminAjaxHandler)
        errors += self._VerifyInheritance(routes._CRON_ROUTES,
                                          handlers.BaseCronHandler)
        errors += self._VerifyInheritance(routes._TASK_ROUTES,
                                          handlers.BaseTaskHandler)
        if errors:
            self.fail('Some handlers do not inherit from the correct classes:\n' + errors)

    def testStrictHandlerMethodRouting(self):
        """Checks that handler functions properly limit applicable HTTP methods."""
        router = webapp2.Router(routes._USER_ROUTES + routes._AJAX_ROUTES +
                                routes._ADMIN_ROUTES + routes._ADMIN_AJAX_ROUTES)
        route_list = router.match_routes + router.build_routes.values()
        failed_routes = []
        while route_list:
            route = route_list.pop()
            if issubclass(route.__class__, MultiRoute):
                route_list += list(route.get_routes())
                continue

            # If the handler is in string from, request the the expected object
            if isinstance(route.handler, basestring):
                route.handler = import_string(route.handler)

            if issubclass(route.handler, webapp2.RedirectHandler):
                continue

            if route.handler_method and not route.methods:
                failed_routes.append('%s (%s)' % (route.template,
                                                  route.handler.__name__))

        if failed_routes:
            self.fail('Some handlers specify a handler_method but are missing a '
                      'methods" attribute and may be vulnerable to XSRF via GET '
                      'requests:\n * ' + '\n * '.join(failed_routes))
