"""
Internal base utilities.
"""

from typing import Optional

import requests
from .exceptions import BaseXToolsException, NotFound

BASE_URL = "https://xtools.wmflabs.org/api"


def url(path: str) -> str:
    """
    Return a full API URL.
    :param path:
    :return:
    """
    return BASE_URL + path


def error_exception(response: dict) -> Optional[BaseXToolsException]:
    """
    Return an optional Exception instance for an error response. Return ``None`` if the given response is not an error.
    :param response: response from the API.
    :return: ``None`` or a ``BaseXToolsException`` (or subclass) instance.
    """
    if "error" not in response:
        return

    error = response["error"]

    # 'error' can be a dict or a string
    if isinstance(error, dict):
        code = error["code"]
        if code == 404:
            return NotFound(error["message"])

        return BaseXToolsException(error["message"], code)

    if error.startswith("No matching result"):
        return NotFound(error)

    return BaseXToolsException(str(error))


def get(path: str):
    r = requests.get(url(path))
    response = r.json()
    exception = error_exception(response)
    if exception:
        raise exception
    return response