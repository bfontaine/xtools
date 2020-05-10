import requests_mock

from xtools import tests, user, exceptions


class TestUser(tests.TestCase):
    def test_pages_created(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/user/pages/project1/foo", json={"pages": {}})
            self.assertEqual({"pages": []},
                             user.pages_created("project1", "foo"))