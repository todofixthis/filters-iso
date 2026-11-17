## Architecture

This is a `phx-filters` extension package. Every filter lives in `src/filters_iso/` and is registered as a `filters.extensions` entry point in `pyproject.toml`. Each filter follows the same pattern, so read an existing one before adding another. A filter imports its third-party library inside `_apply`, so a project that never uses it doesn't load it.

Its user docs are prose in filters' `docs/extension_filters.rst`, in todofixthis/filters: a change to a filter's behaviour goes there too.

## Tests

One test module per filter, of flat pytest functions using the `assert_filter_passes` and `assert_filter_errors` fixtures from the `filters.pytest` plugin. Read an error code from the filter class (`filters_iso.Country.CODE_INVALID`), not from `f.ext`, which types its classes as plain `BaseFilter`.
