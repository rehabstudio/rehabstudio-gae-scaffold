#!/usr/bin/env python
"""Checks if a given git repo has uncommitted or untracked files.

Returns a non-zero exit code if the repo is dirty.
"""
# future imports
from __future__ import absolute_import
from __future__ import print_function

# stdlib imports
import collections
import subprocess
import sys


def run_process(cmd_args, cwd=None):
    """Runs the given process and returns its output and exit code.
    """
    try:
        return subprocess.check_output(cmd_args, stderr=subprocess.STDOUT, cwd=cwd), 0
    except subprocess.CalledProcessError, e:
        return e.output, e.returncode


def check_directory(directory):
    """Uses `git status` to check if the given repo is dirty
    """
    return run_process(['git', 'status', '-s'], directory)


def extract_stats(output):
    """Extract stats from `git status` output
    """
    lines = output.splitlines()
    return collections.Counter([x.split()[0] for x in lines])


def is_dirty(stats):
    return int(bool(sum(stats.values())))


def pretty_print_stats(stats):
    if is_dirty(stats):
        print('Git repository is dirty.')
        for k, v in stats.items():
            print('{0}: {1}'.format(k, v))
    else:
        print('Git repository is clean.')


if __name__ == '__main__':

    # get directory from the command line (required)
    try:
        directory = sys.argv[1]
    except IndexError:
        print('A path is required as the first argument to the script.')
        sys.exit(1)

    # check if we should print stats to stdout.
    try:
        quiet = sys.argv[2] == '--quiet'
    except IndexError:
        quiet = False

    output, _ = check_directory(directory)
    stats = extract_stats(output)
    if not quiet:
        pretty_print_stats(stats)

    sys.exit(is_dirty(stats))
