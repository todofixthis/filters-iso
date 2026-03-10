# Migrate Tests to Pytest Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace `unittest`-based tests with idiomatic pytest flat functions, one module per filter.

**Architecture:** Delete `test/test_filters_iso.py`; create `test/test_country.py`, `test/test_currency.py`, and `test/test_locale.py`. Use the `assert_filter_passes` / `assert_filter_errors` fixtures injected automatically by the `filters.pytest` pytest plugin (from `phx-filters >= 3.5.1`). Add `pytest` as a dev dependency and update `tox` to invoke it.

**Tech Stack:** pytest, phx-filters pytest plugin (`filters.pytest`), uv/tox

---

### Task 1: Add pytest dev dependency and update tox

**Files:**
- Modify: `pyproject.toml`

**Step 1: Add pytest to dev dependencies**

In `pyproject.toml`, add `pytest` to the `[dependency-groups] dev` list (keep alphabetical order):

```toml
[dependency-groups]
dev = [
    "autohooks>=26,<27",
    "autohooks-plugin-black>=23,<24",
    "autohooks-plugin-ruff>=25,<26",
    "black>=26,<27",
    "pytest>=8,<9",
    "tox>=4,<5",
    "tox-uv>=1.23.0,<2",
]
```

**Step 2: Update the tox command**

Change `[tool.tox.env_run_base]` from:

```toml
commands = [["python", "-m", "unittest"]]
```

to:

```toml
commands = [["pytest"]]
```

**Step 3: Sync dependencies**

```bash
uv sync
```

Expected: resolves successfully, `pytest` appears in installed packages.

**Step 4: Verify pytest runs (existing tests still pass via unittest discovery)**

```bash
uv run pytest
```

Expected: pytest finds and runs the existing `test_filters_iso.py` tests. All pass. The session header should include `plugins: phx-filters-3.5.1`.

**Step 5: Commit**

```bash
git add pyproject.toml uv.lock
git commit
```

---

### Task 2: Write test/test_country.py

**Files:**
- Create: `test/test_country.py`
- Reference: `test/test_filters_iso.py` (CountryTestCase — source of truth for test cases)

**Step 1: Create the file**

```python
import filters as f
from filters.pytest import skip_value_check
from iso3166 import Country, countries_by_alpha3


def test_pass_none(assert_filter_passes):
    """
    ``None`` always passes this filter.

    Use ``Required | Country`` if you want to reject ``None``.
    """
    assert_filter_passes(f.ext.Country(), None)


def test_pass_valid_alpha_3(assert_filter_passes):
    """
    The incoming value is a valid ISO-3316-1 alpha-3 country code.
    """
    runner = assert_filter_passes(f.ext.Country(), 'FRA', skip_value_check)

    country = runner.cleaned_data
    assert isinstance(country, Country)
    assert country.name == 'France'


def test_pass_valid_alpha_2(assert_filter_passes):
    """
    The incoming value is a valid ISO-3166-1 alpha-2 country code.
    """
    runner = assert_filter_passes(f.ext.Country(), 'IE', skip_value_check)

    country = runner.cleaned_data
    assert isinstance(country, Country)
    assert country.name == 'Ireland'


def test_pass_case_insensitive(assert_filter_passes):
    """
    The incoming value is basically valid, but it has the wrong case.
    """
    runner = assert_filter_passes(f.ext.Country(), 'arg', skip_value_check)

    country = runner.cleaned_data
    assert isinstance(country, Country)
    assert country.name == 'Argentina'


def test_fail_invalid_code(assert_filter_errors):
    """
    The incoming value is not a valid ISO-3316-1 country code.
    """
    # Surrender is not an option!
    assert_filter_errors(f.ext.Country(), '\u2690', [f.ext.Country.CODE_INVALID])


def test_fail_subdivision(assert_filter_errors):
    """
    Subdivisions are not accepted, even though certain ones are technically
    part of ISO-3166-1.

    After all, the filter is named ``Country``, not ``ISO_3166_1``!
    """
    assert_filter_errors(f.ext.Country(), 'IE-L', [f.ext.Country.CODE_INVALID])


def test_fail_wrong_type(assert_filter_errors):
    """
    The incoming value is not a string.
    """
    assert_filter_errors(f.ext.Country(), ['CHN', 'JPN'], [f.Type.CODE_WRONG_TYPE])


def test_pass_country_object(assert_filter_passes):
    """
    The incoming value is already a :py:class:`Country` object.
    """
    assert_filter_passes(f.ext.Country(), countries_by_alpha3.get('USA'))
```

**Step 2: Run the new tests**

```bash
uv run pytest test/test_country.py -v
```

Expected: all 8 tests pass.

**Step 3: Commit**

```bash
git add test/test_country.py
git commit
```

---

### Task 3: Write test/test_currency.py

**Files:**
- Create: `test/test_currency.py`
- Reference: `test/test_filters_iso.py` (CurrencyTestCase)

**Step 1: Create the file**

```python
import filters as f
from filters.pytest import skip_value_check
from moneyed import Currency, get_currency


def test_pass_none(assert_filter_passes):
    """
    ``None`` always passes this filter.

    Use ``Required | Currency`` if you do want to reject ``None``.
    """
    assert_filter_passes(f.ext.Currency(), None)


def test_pass_valid_code(assert_filter_passes):
    """
    The incoming value is a valid ISO-4217 currency code.
    """
    runner = assert_filter_passes(f.ext.Currency(), 'PEN', skip_value_check)

    currency = runner.cleaned_data
    assert isinstance(currency, Currency)
    assert currency.name == 'Peruvian Sol'


def test_pass_case_insensitive(assert_filter_passes):
    """
    The incoming value is basically valid, but it has the wrong case.
    """
    runner = assert_filter_passes(f.ext.Currency(), 'ars', skip_value_check)

    currency = runner.cleaned_data
    assert isinstance(currency, Currency)
    assert currency.name == 'Argentine Peso'


def test_fail_invalid_code(assert_filter_errors):
    """
    The incoming value is not a valid ISO-4217 currency code.
    """
    # You can't use the currency symbol, silly!
    assert_filter_errors(f.ext.Currency(), '\u00a3', [f.ext.Currency.CODE_INVALID])


def test_fail_wrong_type(assert_filter_errors):
    """
    The incoming value is not a string.
    """
    assert_filter_errors(f.ext.Currency(), ['USD', 'CNY'], [f.Type.CODE_WRONG_TYPE])


def test_pass_currency_object(assert_filter_passes):
    """
    The incoming value is already a :py:class:`moneyed.Currency` object.
    """
    assert_filter_passes(f.ext.Currency(), get_currency(code='USD'))
```

**Step 2: Run the new tests**

```bash
uv run pytest test/test_currency.py -v
```

Expected: all 6 tests pass.

**Step 3: Commit**

```bash
git add test/test_currency.py
git commit
```

---

### Task 4: Write test/test_locale.py

**Files:**
- Create: `test/test_locale.py`
- Reference: `test/test_filters_iso.py` (LocaleTestCase)

**Step 1: Create the file**

```python
import filters as f
from filters.pytest import skip_value_check
from language_tags import tags
from language_tags.Tag import Tag


def test_pass_none(assert_filter_passes):
    """
    ``None`` always passes this filter.

    Use ``Required | Locale`` if you want to reject ``None``.
    """
    assert_filter_passes(f.ext.Locale(), None)


def test_valid_locale(assert_filter_passes):
    """
    Valid locale string is valid.

    References:
      - http://r12a.github.io/apps/subtags/
      - https://pypi.python.org/pypi/language-tags
      - https://github.com/mattcg/language-tags
    """
    runner = assert_filter_passes(f.ext.Locale(), 'en-cmn-Hant-HK', skip_value_check)

    tag = runner.cleaned_data
    assert isinstance(tag, Tag)
    assert tag.valid
    assert str(tag) == 'en-cmn-Hant-HK'
    assert str(tag.language) == 'en'
    assert str(tag.region) == 'HK'
    assert str(tag.script) == 'Hant'


def test_pass_case_insensitive(assert_filter_passes):
    """
    The incoming value is basically valid, except it uses the wrong case.
    """
    runner = assert_filter_passes(f.ext.Locale(), 'Az-ArAb-Ir', skip_value_check)

    tag = runner.cleaned_data
    assert isinstance(tag, Tag)
    assert tag.valid
    assert str(tag) == 'az-Arab-IR'
    assert str(tag.language) == 'az'
    assert str(tag.region) == 'IR'
    assert str(tag.script) == 'Arab'


def test_fail_invalid_value(assert_filter_errors):
    """
    The incoming value generates parsing errors.
    """
    # noinspection SpellCheckingInspection
    runner = assert_filter_errors(
        f.ext.Locale(),
        'sl-Cyrl-YU-rozaj-solba-1994-b-1234-a-Foobar-x-b-1234-a-Foobar',
        [f.ext.Locale.CODE_INVALID],
    )

    # Parse errors included here for demonstration purposes.
    assert runner.filter_messages[''][0].context.get('parse_errors') == [
        # Sorry about the magic values.
        # These are defined in the Tag initialiser, so they're a bit
        # tricky to get at without complicating the test.
        # :py:meth:`Tag.__init__`
        (11, "The subtag 'YU' is deprecated."),
        (8, "Duplicate variant subtag 'solba' found."),
        (8, "Duplicate variant subtag '1994' found."),
    ]


def test_fail_wrong_type(assert_filter_errors):
    """
    The incoming value is not a string.
    """
    assert_filter_errors(f.ext.Locale(), ['en', 'US'], [f.Type.CODE_WRONG_TYPE])


def test_pass_tag_object(assert_filter_passes):
    """
    The incoming value is already a Tag object.
    """
    assert_filter_passes(f.ext.Locale(), tags.tag('en-cmn-Hant-HK'))
```

**Step 2: Run the new tests**

```bash
uv run pytest test/test_locale.py -v
```

Expected: all 6 tests pass.

**Step 3: Commit**

```bash
git add test/test_locale.py
git commit
```

---

### Task 5: Remove old test file, update docs, final verification

**Files:**
- Delete: `test/test_filters_iso.py`
- Delete: `test/__init__.py` (pytest doesn't need it)
- Modify: `AGENTS.md`

**Step 1: Delete the old test file and package marker**

```bash
git rm test/test_filters_iso.py test/__init__.py
```

**Step 2: Update AGENTS.md**

Replace the `## Commands` section with:

```markdown
## Commands

\`\`\`bash
uv run pytest                          # run all tests
uv run pytest test/test_country.py -v  # run one test module
uv run tox -p                          # test across all supported Python versions
\`\`\`
```

Replace the last sentence of `## Architecture`:

```markdown
Tests are flat pytest functions using the `assert_filter_passes` and
`assert_filter_errors` fixtures injected by the `filters.pytest` plugin. One test
module per filter: `test/test_country.py`, `test/test_currency.py`,
`test/test_locale.py`.
```

**Step 3: Run the full test suite**

```bash
uv run pytest -v
```

Expected: 20 tests collected across 3 modules, all pass. Session header includes `plugins: phx-filters-3.5.1`.

**Step 4: Commit**

```bash
git add AGENTS.md
git commit
```
