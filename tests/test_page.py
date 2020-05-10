import requests_mock

from xtools import tests, page, exceptions


class TestProject(tests.TestCase):
    def test_single_page(self):
        with requests_mock.Mocker() as m:
            response = {"some": "info", "here": "too"}
            m.get("m://x/page/articleinfo/en.wikipedia.org/Albert_Einstein", json=response)
            self.assertEqual(response,
                             page.article_info("en.wikipedia.org", "Albert_Einstein"))

            m.get("m://x/page/articleinfo/en.wikipedia.org/i don't exist lol",
                  json={"error": "No matching results found for: i don't exist lol"},
                  status_code=404)
            self.assertRaises(exceptions.NotFound,
                              lambda: page.article_info("en.wikipedia.org", "i don't exist lol"))