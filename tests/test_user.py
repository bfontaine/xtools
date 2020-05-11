import requests_mock

from xtools import tests, user, exceptions


class TestUser(tests.TestCase):
    def test_simple_info(self):
        for what, fn in (
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
        ):
            prefix = "m://x/user/%s" % what

            with requests_mock.Mocker() as m:
                response = {"some": "info", "here": "too"}
                m.get(prefix + "/enwiki/Albert_Einstein", json=response)
                self.assertEqual(response, fn("enwiki", "Albert_Einstein"))

                m.get(prefix + "/enwiki/no",
                      json={"error": "The requested user does not exist"},
                      status_code=404)
                self.assertRaises(exceptions.NotFound, lambda: fn("enwiki", "no"))

    def test_pages_created_empty(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/user/pages/project1/foo", json={"pages": {}})
            self.assertEqual({"pages": []},
                             user.pages_created("project1", "foo"))
            self.assertEqual([],
                             list(user.pages_created_iter("project1", "foo")))

    def test_pages_created_int_title(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/user/pages/project1/foo", json={"pages": {"0": {"page_title": 2040}}})
            self.assertEqual({"pages": [{"page_title": "2040"}]},
                             user.pages_created("project1", "foo"))
            self.assertSequenceEqual([{"page_title": "2040"}],
                                     list(user.pages_created_iter("project1", "foo")))

    def test_pages_created_non_existing_user(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/user/pages/project1/foo", json={"error": "The requested user does not exist"})
            self.assertRaises(exceptions.NotFound,
                              lambda: user.pages_created("project1", "foo"))
            self.assertRaises(exceptions.NotFound,
                              lambda: next(user.pages_created_iter("project1", "foo")))