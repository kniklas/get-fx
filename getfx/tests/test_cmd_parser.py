import pytest
from getfx.cmdparser import parse_getfx


def test_empty_currency():
    assert parse_getfx([]).currency == 'CHF'


@pytest.mark.parametrize('args, expected_currency, expected_date', (
    (['USD', '-d', '2020-01-20'], 'USD', '2020-01-20'),
    (['-d', '2020-01-20'], 'CHF', '2020-01-20'),
    (['USD'], 'USD', None)
))
def test_with_currency_and_date(args, expected_currency, expected_date):
    assert parse_getfx(args).currency == expected_currency
    assert parse_getfx(args).date == expected_date
