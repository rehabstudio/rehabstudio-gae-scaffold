#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""An interactive python shell that uses remote_api.

Used to provide a local python shell that operates against the running local
application server.
"""
# stdlib imports
import distutils.spawn
import os
import sys


def setup_environ():
    """This func will import the required modules and set up enough of an
    appengine environment to let some of our management commands run inside the
    SDK sandbox
    """

    # Find the path on which the SDK is installed
    test_path = distutils.spawn.find_executable('dev_appserver.py')
    if test_path is None:  # pragma: no cover
        print "ERROR: Can't find appengine SDK on your PATH"
        sys.exit(1)
    sdk_path = os.path.dirname(os.readlink(test_path) if os.path.islink(test_path) else test_path)

    # add the SDK path to the system path
    sys.path.insert(0, sdk_path)

    # Use dev_appserver to set up the python path
    if 'google-cloud-sdk' in sdk_path:
        sdk_path = os.path.join(os.path.split(sdk_path)[0], 'platform', 'google_appengine')
        sys.path.insert(0, os.path.abspath(sdk_path))
        from dev_appserver import fix_sys_path
    else:
        from dev_appserver import fix_sys_path
    fix_sys_path()


# fix the environment
setup_environ()

# import the os compatibility shim
from google.appengine.tools import os_compat

# third-party imports
import IPython
from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.tools import appengine_rpc


BANNER = """App Engine remote_api shell
All SDK and application modules should be on the path and importable.\
"""


def auth_func():
    return ('xxx@xxx', 'xxx')


def remote_api_shell(servername, appid, path, secure, rpc_server_factory):
    """Actually run the remote_api_shell.
    """

    remote_api_stub.ConfigureRemoteApi(appid, path, auth_func,
                                       servername=servername,
                                       save_cookies=True, secure=secure,
                                       rpc_server_factory=rpc_server_factory)
    remote_api_stub.MaybeInvokeAuthentication()

    os.environ['SERVER_SOFTWARE'] = 'Development (remote_api_shell)/1.0'

    # ensure our app is on the python path
    sys.path.insert(0, '/src-server')
    # run an embedded IPython shell in the current context
    IPython.embed(header=BANNER)


def main():
    """run python shell.
    """
    remote_api_shell('localhost:8080', 'dev~gae-scaffold', '/_ah/remote_api', False, appengine_rpc.HttpRpcServer)


if __name__ == '__main__':
  main()
