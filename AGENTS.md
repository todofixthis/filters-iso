# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run pytest                          # run all tests
uv run pytest test/test_country.py     # run one test module
uv run tox -p                          # test across all supported Python versions
```

## Architecture

This is a `phx-filters` extension package. All filters live in `filters_iso/__init__.py` and are registered as `filters.extensions` entry points. Each filter follows the same pattern — read any existing filter to understand it before adding a new one.

Tests are flat pytest functions using the `assert_filter_passes` and
`assert_filter_errors` fixtures injected by the `filters.pytest` plugin. One test
module per filter: `test/test_country.py`, `test/test_currency.py`,
`test/test_locale.py`.
