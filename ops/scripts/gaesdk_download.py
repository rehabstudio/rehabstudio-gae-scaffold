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


def ensure_directory(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def unpack_zipfile(filename, extract_dir, progress_filter=lambda x, y: y):
    """Unpack zip `filename` to `extract_dir`
    """

    z = zipfile.ZipFile(filename)
    try:
        for info in z.infolist():
            name = info.filename

            # don't extract absolute paths or ones with .. in them
            if name.startswith('/') or '..' in name:
                continue

            target = os.path.join(extract_dir, *name.split('/'))
            target = progress_filter(name, target)
            if not target:
                continue
            if name.endswith('/'):
                # directory
                ensure_directory(target)
            else:
                # file
                ensure_directory(target)
                data = z.read(info.filename)
                f = open(target, 'wb')
                try:
                    f.write(data)
                finally:
                    f.close()
                    del data
            unix_attributes = info.external_attr >> 16
            if unix_attributes:
                os.chmod(target, unix_attributes)
    finally:
        z.close()


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

    unpack_zipfile(zip_path, '/opt/')


if __name__ == '__main__':

    # get version number from the command line (required)
    try:
        version_number = sys.argv[1]
    except IndexError:
        print('A version number is required as the first argument to the script.')
        sys.exit(1)

    download_sdk(version_number)
