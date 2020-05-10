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
    if "error" not in response:
        return

    error = response["error"]
    code = error["code"]
    if code == 404:
        return NotFound(error["message"])

    return BaseXToolsException(error["message"], code)


def get(path: str):
    r = requests.get(url(path))
    response = r.json()
    exception = error_exception(response)
    if exception:
        raise exception
    return response