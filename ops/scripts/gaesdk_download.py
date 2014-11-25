#!/usr/bin/env python
"""Downloads a given version of the appengine SDK and unzips to /opt/.

A version number must be passed to the script at runtime.  Derived from Peter
Hudec's gae_installer package: https://github.com/peterhudec/gae_installer
"""
# future imports
from __future__ import absolute_import
from __future__ import print_function

# stdlib imports
import os
import sys
import tempfile
import urllib2
import zipfile


def _get_download_url(version, deprecated=False):
    """Return a URL for a given SDK version.
    """
    base_url = 'https://storage.googleapis.com/appengine-sdks/{0}/google_appengine_{1}.zip'
    if deprecated:
        return base_url.format('deprecated/{0}'.format(version.replace('.', '')), version)
    else:
        return base_url.format('featured', version)


def _print_deprecation_warning(version):
    """Print a deprecation warning to the user's terminal.
    """
    print()
    print('########## WARNING!! ##########')
    print()
    print('SDK version {0} is deprecated!'.format(version))
    print('Check for the latest release and update your Dockerfile')
    print()
    print('    https://cloud.google.com/appengine/downloads ')
    print()


def download_sdk(version):
    """Downloads the GAE SDK.
    """

    try:
        response = urllib2.urlopen(_get_download_url(version))
    except urllib2.HTTPError, e:
        if e.code == 404:
            _print_deprecation_warning(version)
            response = urllib2.urlopen(_get_download_url(version, deprecated=True))
        else:
            raise

    zip_path = os.path.join(tempfile.gettempdir(), 'google_appengine_{0}.zip'.format(version))
    with open(zip_path, 'w') as f:
        f.write(response.read())

    zipfile.ZipFile(zip_path).extractall('/opt/')


if __name__ == '__main__':

    # get version number from the command line (required)
    try:
        version_number = sys.argv[1]
    except IndexError:
        print('A version number is required as the first argument to the script.')
        sys.exit(1)

    download_sdk(version_number)
