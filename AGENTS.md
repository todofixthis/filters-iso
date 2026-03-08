# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run python -m unittest                                         # run all tests
uv run python -m unittest test.test_filters_iso.CountryTestCase   # run one test class
uv run tox -p                                                     # test across all supported Python versions
```

## Architecture

This is a `phx-filters` extension package. All filters live in `filters_iso/__init__.py` and are registered as `filters.extensions` entry points. Each filter follows the same pattern — read any existing filter to understand it before adding a new one.

Tests extend `BaseFilterTestCase` from `phx-filters`.
