---
status: Accepted
date: 2026-03-10
scope: [test/]
summary: Migrate tests from unittest.TestCase to flat pytest functions, one module per filter.
---

# 001: Migrate Tests to Pytest

## Context

Tests have historically used `unittest.TestCase` via `BaseFilterTestCase` from `phx-filters`.
`phx-filters` v3.5.0 introduced a pytest plugin (`filters.pytest`), packaged for
distribution via the `pytest11` entry point in v3.5.1. The `phx-filters-*` library
ecosystem is moving to pytest-native patterns, and downstream packages such as
`phx-filters-django` are expected to follow. Aligning `phx-filters-iso` keeps the
ecosystem consistent.

## Options

### Option 1: Do nothing

Keep `unittest.TestCase` / `BaseFilterTestCase` and run tests with `python -m unittest`.

**Pros:** No migration effort.
**Cons:** Diverges from the direction of the `phx-filters-*` ecosystem.
**Risks:** Accumulates drift as other packages in the ecosystem migrate.

### Option 2: Migrate to pytest flat functions (Accepted)

Replace each `class XxxTestCase(BaseFilterTestCase)` with a set of top-level functions
(`test_country_*`, `test_currency_*`, `test_locale_*`). Use the injected
`assert_filter_passes` and `assert_filter_errors` fixtures. Split into one module per
filter (`test_country.py`, `test_currency.py`, `test_locale.py`). Run tests with `pytest`.

**Pros:** Idiomatic pytest; consistent with `phx-filters` and the wider ecosystem; one
module per filter is easier to navigate.
**Cons:** More lines changed than a minimal migration.
**Risks:** Low — the plugin API is stable and already in use upstream.

### Option 3: Migrate to pytest class-based (no inheritance)

Keep the class grouping but drop `BaseFilterTestCase`, injecting fixtures as method
parameters.

**Pros:** Conservative change; preserves visual grouping.
**Cons:** Still carries unnecessary class ceremony; diverges from upstream style.
**Risks:** Low, but produces a halfway house that will likely need revisiting.

## Decision

Adopt flat pytest functions (Option 2), split into one module per filter. This matches the
direction set by `phx-filters` v3.5.0 and establishes a pattern that `phx-filters-django`
and other downstream packages can follow.

## Consequences

- `pytest` added as a dev dependency; `python -m unittest` replaced by `pytest` in `tox`
  and developer docs.
- `test/test_filters_iso.py` replaced by `test/test_country.py`, `test/test_currency.py`,
  and `test/test_locale.py`.
- `BaseFilterTestCase` no longer used in this package; minimum `phx-filters` version raised to `>= 3.5.1`.
- Future filter additions follow the same flat-function, one-module-per-filter pattern.
