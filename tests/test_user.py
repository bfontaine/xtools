import requests_mock

from xtools import tests, user, exceptions


class TestUser(tests.TestCase):
    def test_pages_created_empty(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/user/pages/project1/foo", json={"pages": {}})
            self.assertEqual({"pages": []},
                             user.pages_created("project1", "foo"))

    def test_pages_created_int_title(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/user/pages/project1/foo", json={"pages": {"0": {"page_title": 2040}}})
            self.assertEqual({"pages": [{"page_title": "2040"}]},
                             user.pages_created("project1", "foo"))