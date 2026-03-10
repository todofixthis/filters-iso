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
