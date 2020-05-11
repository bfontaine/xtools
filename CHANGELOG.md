# `xtools` Changelog

## 0.1.0 (2020/05/11)

* Fix `user.steward_statistics` URL
* Fix default namespaces in `user` functions
* Retry up to 3 times on proxy errors
* Exceptions can now be compared using `==`
* Import exceptions under `xtools.*` (e.g. `xtools.NotFound` for `xtools.exceptions.NotFound`)

## 0.0.4 (2020/05/11)

* Add full support for the User API
* Raise a `NotFound` exception instead of `BaseXToolsException` when a user
  doesn’t exist
* Small docstrings improvements

## 0.0.3 (2020/05/11)

* Force the page titles in `user.page_created` as strings. The API sometimes
  return them as ints (e.g. [2040][]).

[2040]: https://fr.wikipedia.org/wiki/2040

## 0.0.2 (2020/05/10)

* Fix `user.pages_created` and `user.pages_created_iter` for users with no
  created pages.

## 0.0.1 (2020/05/10)

First initial release.

* Full support for the Page, Project, and Quote APIs
* Partial support for the User API
