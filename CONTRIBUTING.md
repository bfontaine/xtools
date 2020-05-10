# Contributing to `xtools`

## Setup

    pip3 install -r requirements.txt

## Tests

Run unit tests with:

    python3 tests/test.py

Check Python warnings with:

    python3 -Wall -c 'import xtools'

## Release a new version

To release a new version:

1. Ensure you have setup [`twine`](https://pypi.org/project/twine/)
2. Bump up the version number in `setup.py` and `xtools/__init__.py`, e.g. `0.1.0`
3. Fill the `CHANGELOG.md`
4. Commit and tag
5. Clean your `dist/` directory if it already exists
6. Package the release: `python setup.py sdist bdist_wheel`
7. Check the package: `twine check dist/*`
8. Upload the package: `twine upload dist/*`
9. Push