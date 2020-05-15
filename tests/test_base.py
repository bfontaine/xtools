import requests_mock
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

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

            ("/x/2000-01-01/a", "/{a}/{start}/{b}", [("a", "", "x"), ("start", "", ""), ("b", "a", "x")]),
            ("/x/2050-12-31/a", "/{a}/{end}/{b}", [("a", "", "x"), ("end", "", ""), ("b", "a", "x")]),
            ("/x/%3F", "/{a}/{b}", [("a", "", "x"), ("b", "?", "")]),
        ):
            self.assertEqual(expected, base.build_path(path_format, path_params), path_format)

    def test_error_exception(self):
        for expected, response in (
            (None, {}),
            (exceptions.NotFound("foo"), {"error": {"code": 404, "message": "foo"}}),
            (exceptions.BaseXToolsException("bar", 403), {"error": {"code": 403, "message": "bar"}}),

            (exceptions.NotFound("No matching result"), {"error": "No matching result"}),
            (exceptions.NotFound("X is not a valid project"), {"error": "X is not a valid project"}),
            (exceptions.NotFound("The requested user does not exist"), {"error": "The requested user does not exist"}),
            (exceptions.TooManyEdits("User has made too many edits!"), {"error": "User has made too many edits!"}),
            (exceptions.BaseXToolsException("foobar"), {"error": "foobar"}),
        ):
            self.assertEqual(expected, base.error_exception(response), response)

    def test_get(self):
        with requests_mock.Mocker() as m:
            response = {"foo": "bar"}
            m.get("m://x/foo", json=response)
            self.assertEqual(response, base.get("/foo"))

    def test_get_404_json(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/a", json={"error": {"code": 404, "message": "foo"}}, status_code=404)
            self.assertRaises(exceptions.NotFound, lambda: base.get("/a"))

    def test_get_404_html(self):
        with requests_mock.Mocker() as m:
            m.get("m://x/a", text='<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">...', status_code=404)
            self.assertRaises(HTTPError, lambda: base.get("/a"))

    def test_get_200_html(self):
        # Shouldn't happen in practice, but let's be safe
        with requests_mock.Mocker() as m:
            m.get("m://x/a", text='<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">...')
            self.assertRaises(JSONDecodeError, lambda: base.get("/a"))

    def test_get_502(self):
        with requests_mock.Mocker() as m:
            response = {"foo": "bar"}

            error = {"text": '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">...', "status_code": 502}
            ok = {"json": response}

            m.get("m://x/foo1", [error, ok])
            self.assertEqual(response, base.get("/foo1", retry_delay=0))

            m.get("m://x/foo2", [error, error, ok])
            self.assertEqual(response, base.get("/foo2", retry_delay=0))

            m.get("m://x/fooX", [error])
            self.assertRaises(Exception, lambda: base.get("/fooX", retry_delay=0))