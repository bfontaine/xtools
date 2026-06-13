from collections.abc import Generator

import pytest

from xtools import base

TEST_URL_PREFIX = "m://x"


@pytest.fixture(autouse=True)
def set_test_url_prefix() -> Generator[None, None, None]:
    base_url = base.BASE_URL
    base.BASE_URL = "m://x"
    yield
    base.BASE_URL = base_url
