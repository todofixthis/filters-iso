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
