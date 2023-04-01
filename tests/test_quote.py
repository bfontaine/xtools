import pytest
import requests_mock

from xtools import quote, exceptions


def test_random_quote():
    with requests_mock.Mocker() as m:
        m.get("m://x/quote/random", json={"42": "something"})
        assert quote.random_quote() == quote.Quote(42, "something")


def test_get_quote():
    with requests_mock.Mocker() as m:
        m.get("m://x/quote/43", json={"43": "something"})
        assert quote.single_quote(43) == quote.Quote(43, "something")

        m.get("m://x/quote/1000",
              json={"error": {"code": 404, "message": "No quote found with ID 1000"}},
              status_code=404)
        with pytest.raises(exceptions.NotFound):
            quote.single_quote(1000)


def test_all_quotes():
    with requests_mock.Mocker() as m:
        m.get("m://x/quote/all", json={"1": "one", "2": "two", "3": "three"})
        assert quote.all_quotes() == [quote.Quote(1, "one"), quote.Quote(2, "two"), quote.Quote(3, "three")]
