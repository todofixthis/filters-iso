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
    The incoming value is a valid ISO-3166-1 alpha-3 country code.
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
    The incoming value is not a valid ISO-3166-1 country code.
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
