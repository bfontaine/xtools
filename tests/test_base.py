import requests_mock

from xtools import tests, base, exceptions


class TestPage(tests.TestCase):
    def test_build_path(self):
        for expected, path_format, path_params in (
            ("/foo", "/foo", []),
            ("/foo", "/{a}", [("a", "foo", "")]),
            ("/foo", "/{a}", [("a", "foo", "bar")]),
            ("/foo", "/{a}/{b}/{c}", [("a", "foo", "x"), ("b", "", "x"), ("c", "", "x")]),

            ("", "/{a}", [("a", None, "foo")]),

            ("", "/{a}/{b}", [("a", None, "foo"), ("b", None, "")]),
            ("", "/{a}/{b}", [("a", None, "foo"), ("b", None, "bar")]),

            ("/foo/qux", "/{a}/{b}", [("a", None, "foo"), ("b", "qux", "bar")]),
            ("/x/x/c", "/{a}/{b}/{c}", [("a", "", "x"), ("b", "", "x"), ("c", "c", "x")]),
            ("/a/x/c", "/{a}/{b}/{c}", [("a", "a", "x"), ("b", "", "x"), ("c", "c", "x")]),
            ("/x/b/c", "/{a}/{b}/{c}", [("a", "", "x"), ("b", "b", "x"), ("c", "c", "x")]),
            ("/a", "/{a}/{b}/{c}", [("a", "a", "x"), ("b", None, "x"), ("c", None, "x")]),
            ("/x/B", "/{a}/{b}/{c}", [("a", "", "x"), ("b", "B", "x"), ("c", "", "x")]),
        ):
            self.assertEqual(expected, base.build_path(path_format, path_params), path_format)

    def test_get(self):
        with requests_mock.Mocker() as m:
            response = {"foo": "bar"}
            m.get("m://x/foo", json=response)
            self.assertEqual(response, base.get("/foo"))

    def test_get_502_one_retry(self):
        with requests_mock.Mocker() as m:
            response = {"foo": "bar"}
            m.get("m://x/foo",
                  [{"text": '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">...', "status_code": 502},
                   {"json": response}])
            self.assertEqual(response, base.get("/foo"))