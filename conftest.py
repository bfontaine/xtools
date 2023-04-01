import pytest

from xtools import base

TEST_URL_PREFIX = "m://x"


@pytest.fixture(autouse=True)
def set_test_url_prefix():
    base_url = base.BASE_URL
    setattr(base, "BASE_URL", "m://x")
    yield
    setattr(base, "BASE_URL", base_url)
