import pytest
import requests_mock

from xtools import page, exceptions


@pytest.mark.parametrize(
    "what,fn",
    [
        ("articleinfo", page.article_info),
        ("prose", page.prose),
        ("links", page.links),
        ("top_editors", page.top_editors),
        ("assessments", lambda p, a: page.assessments(p, [a]))
    ])
def test_simple_info(what, fn):
    prefix = "m://x/page/%s" % what

    with requests_mock.Mocker() as m:
        response = {"some": "info", "here": "too"}
        m.get(prefix + "/en.wikipedia.org/Albert_Einstein", json=response)
        assert fn("en.wikipedia.org", "Albert_Einstein") == response

        m.get(prefix + "/en.wikipedia.org/i%20don%27t%20exist%20lol",
              json={"error": "No matching results found for: i don't exist lol"},
              status_code=404)
        with pytest.raises(exceptions.NotFound):
            fn("en.wikipedia.org", "i don't exist lol")
