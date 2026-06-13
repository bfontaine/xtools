"""
Internal base utilities.
"""
import time
from collections.abc import Sequence
from json.decoder import JSONDecodeError
from typing import Any
from urllib.parse import quote as urlquote

import requests

from .exceptions import BaseXToolsException, NotFound, TooManyEdits

BASE_URL = "https://xtools.wmflabs.org/api"
START_TIME = "2000-01-01"
END_TIME = "2050-12-31"


def url(path: str) -> str:
    """
    Return a full API URL.
    :param path:
    :return:
    """
    return BASE_URL + path


def error_exception(response: dict[str, Any]) -> BaseXToolsException | None:
    """
    Return an optional Exception instance for an error response. Return ``None`` if the given response is not an error.
    :param response: response from the API.
    :return: ``None`` or a ``BaseXToolsException`` (or subclass) instance.
    """
    if "error" not in response:
        return None

    error = response["error"]

    # 'error' can be a dict or a string
    if isinstance(error, dict):
        code = error["code"]
        if code == 404:
            return NotFound(error["message"])

        return BaseXToolsException(error["message"], code)

    if error.startswith("No matching result") \
            or error.endswith("is not a valid project") \
            or error == "The requested user does not exist":
        return NotFound(error)

    if error.startswith("User has made too many edits!"):
        return TooManyEdits(error)

    return BaseXToolsException(str(error))


def get(path: str, params: dict[str, Any] | None = None, retry: int = 3, retry_delay: int = 1) -> dict[str, Any]:
    """
    Perform a GET request against the API.
    :param path:
    :param params:
    :param retry:
    :param retry_delay:
    :return:
    """
    r = requests.get(url(path), params=params)
    # 'Proxy error'
    if r.status_code == 502:
        if retry > 0:
            time.sleep(retry_delay)
            return get(path, params, retry - 1)
        r.raise_for_status()

    try:
        response: dict[str, Any] = r.json()
    except JSONDecodeError as e:
        r.raise_for_status()
        raise e

    exception = error_exception(response)
    if exception:
        raise exception
    return response


def build_path(path_format: str, params: Sequence[tuple[str, Any, str]]) -> str:
    """
    Build a path for the XTools API.

    Examples:

        >>> build_path("/{a}", [("a", "foo", "bar")])
        "/foo"
        >>> build_path("/{a}", [("a", "", "bar")])
        "/bar"
        >>> build_path("/{a}/{b}/{c}", [("a", "", "x"), ("b", "B", "x"), ("c", "", "x")])
        "/x/B"

    :param path_format:
    :param params:
    :return:
    """
    params_dict: dict[str, str] = {}

    def has_more(index: int) -> bool:
        for _, val, _ in params[index + 1:]:
            if val:
                return True
        return False

    for i, (name, value, default) in enumerate(params):
        if value:
            param_value = str(value)
        else:
            param_value = ""

            if has_more(i):
                if default:
                    param_value = default
                # safe defaults
                elif name == "start":
                    param_value = START_TIME
                elif name == "end":
                    param_value = END_TIME

        params_dict[name] = urlquote(param_value)

    path = path_format.format(**params_dict).rstrip("/")
    return path
