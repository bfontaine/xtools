import requests_mock

from xtools import tests, page, exceptions


class TestPage(tests.TestCase):
    def test_simple_info(self):
        for what, fn in (
            ("articleinfo", page.article_info),
            ("prose", page.prose),
            ("links", page.links),
            ("top_editors", page.top_editors),
            ("assessments", lambda p, a: page.assessments(p, [a]))
        ):
            prefix = "m://x/page/%s" % what

            with requests_mock.Mocker() as m:
                response = {"some": "info", "here": "too"}
                m.get(prefix + "/en.wikipedia.org/Albert_Einstein", json=response)
                self.assertEqual(response,
                                 fn("en.wikipedia.org", "Albert_Einstein"))

                m.get(prefix + "/en.wikipedia.org/i don't exist lol",
                      json={"error": "No matching results found for: i don't exist lol"},
                      status_code=404)
                self.assertRaises(exceptions.NotFound,
                                  lambda: fn("en.wikipedia.org", "i don't exist lol"))