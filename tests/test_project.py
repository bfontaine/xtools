import pytest
import requests_mock

from xtools import project, exceptions


@pytest.mark.parametrize(
    "what,fn",
    [
        ("normalize", project.normalize_project),
        ("namespaces", project.namespaces),
        ("assessments", project.page_assessments),
        ("automated_tools", project.automated_tools),
        ("admins_groups", project.admins_and_user_groups),
        ("admin_stats", project.admin_statistics),
        ("patroller_stats", project.patroller_statistics),
        ("steward_stats", project.steward_statistics),
    ])
def test_simple_info(what, fn):
    prefix = "m://x/project/%s" % what

    with requests_mock.Mocker() as m:
        response = {"some": "info", "here": "too"}
        m.get(prefix + "/project1", json=response)
        assert fn("project1") == response

        m.get(prefix + "/en.wikipe",
              json={"error": "en.wikipe is not a valid project"},
              status_code=404)
        with pytest.raises(exceptions.NotFound):
            fn("en.wikipe")


def test_assessments():
    with requests_mock.Mocker() as m:
        response = {"foo": "qux"}
        m.get("m://x/project/assessments", json=response)
        assert project.page_assessments_configuration() == response
