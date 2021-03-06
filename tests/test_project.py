import requests_mock

from xtools import tests, project, exceptions


class TestProject(tests.TestCase):
    def test_simple_info(self):
        for what, fn in (
            ("normalize", project.normalize_project),
            ("namespaces", project.namespaces),
            ("assessments", project.page_assessments),
            ("automated_tools", project.automated_tools),
            ("admins_groups", project.admins_and_user_groups),
            ("admin_stats", project.admin_statistics),
            ("patroller_stats", project.patroller_statistics),
            ("steward_stats", project.steward_statistics),
        ):
            prefix = "m://x/project/%s" % what

            with requests_mock.Mocker() as m:
                response = {"some": "info", "here": "too"}
                m.get(prefix + "/project1", json=response)
                self.assertEqual(response,
                                 fn("project1"))

                m.get(prefix + "/en.wikipe",
                      json={"error": "en.wikipe is not a valid project"},
                      status_code=404)
                self.assertRaises(exceptions.NotFound,
                                  lambda: fn("en.wikipe"))

    def test_assessments(self):
        with requests_mock.Mocker() as m:
            response = {"foo": "qux"}
            m.get("m://x/project/assessments", json=response)
            self.assertEqual(response, project.page_assessments_configuration())