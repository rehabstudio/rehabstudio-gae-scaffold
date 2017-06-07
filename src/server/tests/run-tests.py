#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test runner for gae-scaffold-redux
"""
# stdlib imports
import distutils.spawn
import os
import sys

# third-party imports
import nose

# Fix the path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, base_dir)

# this looks like an unused import, but we're only using it to do some path
# manipulation on import so you can safely ignore it (even though your linter
# may complain)
import appengine_config


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
    # import `api_fixer` to monkey patch a bunch of python stdlib apis with safe defaults
    from app.base import api_fixer


if __name__ == '__main__':

    # setup our appengine environment so we can import the libs we need for our tests,
    # we need to do this first so we can import the stubs from testbed
    setup_environ()

    res = nose.run(argv=[
        'run-tests.py',
        '-v',
        '--with-coverage',
        '--cover-erase',
        '--cover-package=app',
        '--cover-html',
        '--cover-html-dir=/home/aeuser/build/coverage',
        '--with-xunit',
        '--xunit-file=/home/aeuser/build/tests.xml',
        '--with-yanc',
        '--logging-level=INFO'
    ])
    sys.exit(int(not res))
