"""Common network-related functionality
"""
# stdlib imports
import logging

# third-party imports
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

# local imports
from .exceptions import retry_on_exception


class BadResponseError(Exception):
    pass


@retry_on_exception((
    BadResponseError,
    urlfetch_errors.DeadlineExceededError,
    urlfetch_errors.DownloadError,
), tries=3, delay=0.1, backoff=2)
def make_request(url, **urlfetch_params):
    """Make a simple HTTP request to the given URL and return the result
    """
    logging.info('HTTP request: {0}'.format(url))
    response = urlfetch.fetch(url, **urlfetch_params)
    if response.status_code >= 500:
        logging.error(response.content)
        raise BadResponseError(response.status_code)
    return response
