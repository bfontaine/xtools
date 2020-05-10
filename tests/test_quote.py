import requests_mock

from unittest import TestCase

from xtools import base, quote, exceptions

TEST_URL_PREFIX = "m://x"


class TestProject(TestCase):
    def setUp(self):
        self.base_url = base.BASE_URL
        setattr(base, "BASE_URL", TEST_URL_PREFIX)

    def tearDown(self):
        setattr(base, "BASE_URL", self.base_url)

    def test_random_quote(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/quote/random", json={"42": "something"})
            self.assertEqual(quote.Quote(42, "something"),
                             quote.random_quote())

    def test_get_quote(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/quote/43", json={"43": "something"})
            self.assertEqual(quote.Quote(43, "something"),
                             quote.single_quote(43))

            m.get("m://x/quote/1000",
                  json={"error": {"code": 404, "message": "No quote found with ID 1000"}},
                  status_code=404)
            self.assertRaises(exceptions.NotFound,
                              lambda: quote.single_quote(1000))
