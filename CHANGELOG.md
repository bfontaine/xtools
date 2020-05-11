# `xtools` Changelog

## Unreleased

* Raise a `NotFound` exception instead of `BaseXToolsException` when a user
  doesn’t exist

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
