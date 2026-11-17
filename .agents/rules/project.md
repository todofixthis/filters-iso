## Architecture

This is a `phx-filters` extension package. Read an existing filter before adding one. To add a filter:

- write its class in `src/filters_iso/__init__.py`, where every filter lives, and add it to `__all__`;
- register it as a `filters.extensions` entry point in `pyproject.toml`, named after the class;
- add its third-party library with `uv add --bounds major <package>`, and import that library inside `_apply`, so a project that never uses the filter doesn't load it.

The entry point and the filter's dependencies are this project's own content in the template-owned `pyproject.toml`, so edit them here.

Its user docs are prose in todofixthis/filters' `docs/extension_filters.rst`. A new filter needs a section there and a bullet in this repo's `README.rst`; a changed one needs its section updated. Where this session doesn't have filters checked out, list the docs change under a "Docs for todofixthis/filters" heading in the PR description, and tell the person you're working with.

## Tests

One module per filter, `test/test_<filter>.py`, of flat pytest functions using the `assert_filter_passes` and `assert_filter_errors` fixtures from the `filters.pytest` plugin. Construct the filter through the registry (`f.ext.Country()`), which is the only check that its entry point resolves, but read its error codes from the class (`filters_iso.Country.CODE_INVALID`): `f.ext` types its classes as plain `BaseFilter`, which has no `CODE_INVALID`.

The existing tests' multi-line docstrings predate `.agents/rules/testing.md`; write new ones to its one-line rule.
