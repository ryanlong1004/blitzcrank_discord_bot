import requests

import logging

from requests.models import Response

logger: logging.Logger = logging.getLogger(__name__)


class LimitExceededWarning(Exception):
    """Exception raised for errors in the input."""

    pass


def fetch_html(url: str) -> str:
    return requests.get(url).json()["items"]
