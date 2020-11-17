from argparse import ArgumentParser
from unittest.mock import patch

import pytest
from getfx.parser import parse_getfx


def test_empty_currency():
    assert parse_getfx().currency == 'CHF'


# This test is failing due to error raised:
# AttributeError: 'list' object has no attribute 'parse_known_args' when
# patched method: `parse_args` is called
@pytest.mark.xfail
def test_USD_currency():
    test_args = ["USD"]
    #  import wdb; wdb.set_trace()
    with patch.object(ArgumentParser, 'parse_args',
                      return_value=ArgumentParser.parse_args(test_args)):
        testobj = parse_getfx()
        assert testobj.currency == 'USD'
        #  assert mock_method.assert_called()


@pytest.mark.parametrize('args, expected_currency, expected_date', (
    (['USD', '-d', '2020-01-20'], 'USD', '2020-01-20'),
    (['-d', '2020-01-20'], 'CHF', '2020-01-20'),
    (['USD'], 'USD', None)
))
def test_with_currency_and_date(args, expected_currency, expected_date):
    assert parse_getfx(args).currency == expected_currency
    assert parse_getfx(args).date == expected_date
