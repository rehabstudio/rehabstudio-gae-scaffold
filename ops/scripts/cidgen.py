#!/usr/bin/env python
"""Generate a unique ID and write it to a file

We can use it to create unique, per-project containers without requiring the
user to modify any settings unless they want to do so.
"""
# stdlib imports
import os
import uuid
import sys


def main():
    _path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'output', '.cid')
    if not os.path.exists(_path):
        with open(_path, 'w') as f:
            f.write(str(uuid.uuid4()))
    with open(_path, 'r') as f:
        _cid = f.read()
    sys.stdout.write(_cid)


if __name__ == '__main__':

    main()
