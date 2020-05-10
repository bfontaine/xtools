import requests_mock

from xtools import tests, quote, exceptions


class TestProject(tests.TestCase):
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
