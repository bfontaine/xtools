import pytest
import requests_mock

from xtools import user, exceptions


@pytest.mark.parametrize(
    "what,fn",
    [
        ("simple_editcount", user.simple_edit_count),
        ("pages_count", user.number_of_pages_created),
        ("automated_editcount", user.automated_edit_counter),
        ("nonautomated_edits", user.non_automated_edits),
        ("automated_edits", user.automated_edits),
        ("edit_summaries", user.edit_summaries),
        ("top_edits", user.top_edits),
        ("log_counts", user.log_counts),
        ("namespace_totals", user.namespace_totals),
        ("month_counts", user.month_counts),
        ("timecard", user.time_card),
    ])
def test_simple_info(what, fn):
    prefix = "m://x/user/%s" % what

    with requests_mock.Mocker() as m:
        response = {"some": "info", "here": "too"}
        m.get(prefix + "/enwiki/Albert_Einstein", json=response)
        assert fn("enwiki", "Albert_Einstein") == response

        m.get(prefix + "/enwiki/no",
              json={"error": "The requested user does not exist"},
              status_code=404)
        with pytest.raises(exceptions.NotFound):
            fn("enwiki", "no")


def test_pages_created_empty():
    with requests_mock.Mocker() as m:
        m.get("m://x/user/pages/project1/foo", json={"pages": {}})
        assert user.pages_created("project1", "foo") == {"pages": []}
        assert list(user.pages_created_iter("project1", "foo")) == []


def test_pages_created_int_title():
    with requests_mock.Mocker() as m:
        m.get("m://x/user/pages/project1/foo", json={"pages": {"0": {"page_title": 2040}}})
        assert user.pages_created("project1", "foo") == {"pages": [{"page_title": "2040"}]}
        assert list(user.pages_created_iter("project1", "foo")) == [{"page_title": "2040"}]


def test_pages_created_non_existing_user():
    with requests_mock.Mocker() as m:
        m.get("m://x/user/pages/project1/foo", json={"error": "The requested user does not exist"})
        with pytest.raises(exceptions.NotFound):
            user.pages_created("project1", "foo")
        with pytest.raises(exceptions.NotFound):
            next(user.pages_created_iter("project1", "foo"))


def test_pages_created_funky_username():
    with requests_mock.Mocker() as m:
        m.get("m://x/user/pages/project1/%3Fhello", json={"pages": {}})
        assert user.pages_created("project1", "?hello") == {"pages": []}
        assert list(user.pages_created_iter("project1", "?hello")) == []
