import requests
from unittest.mock import patch

import pytest
from getfx import GetFx


STANDARD_RESPONSE_LIST = ["CHF", "203/A/NBP/2020", "2020-10-16", 4.2571]


class ResponseGetMock(object):

    def __init__(self, code):
        self.status_code = code

    def json(self):
        json_response = {"table": "A",
                         "currency": "frank szwajcarski",
                         "code": "CHF",
                         "rates": [{
                             "no": "203/A/NBP/2020",
                             "effectiveDate": "2020-10-16",
                             "mid": 4.2571}]}
        return json_response


@pytest.fixture
def getfx():
    getfx = GetFx()
    yield getfx  # use generator to perform teardown
    getfx._delete()


def test_getfx_initialization(getfx):
    assert getfx


@pytest.mark.parametrize("currency, date, expected_url", (
    ("CHF", None, "http://api.nbp.pl/api/exchangerates/rates/A/CHF"),
    ("CHF", "2020-10-16",
     "http://api.nbp.pl/api/exchangerates/rates/A/CHF/2020-10-16"),
    ("EUR", None, "http://api.nbp.pl/api/exchangerates/rates/A/EUR"),
    ("USD", None, "http://api.nbp.pl/api/exchangerates/rates/A/USD")
 ))
def test_URL_for_currency(getfx, currency, date, expected_url):
    assert getfx._get_request_url(currency, date) == expected_url


@patch.object(requests, 'get', return_value=ResponseGetMock(404))
def test_mocked_URL_exception(mock_object, getfx):
    with pytest.raises(Exception):
        getfx._get_response("R")
    assert mock_object


@patch.object(requests, 'get', return_value=ResponseGetMock(200))
def test_mocked_json(mock_object, getfx):
    getfx._get_response("CHF")
    assert getfx._json_resp['mid'] == 4.2571


@pytest.mark.parametrize("currency, date, expected_result", (
    ("CHF", None, STANDARD_RESPONSE_LIST),
    ("CHF", "2020-10-16", STANDARD_RESPONSE_LIST)
))
@patch.object(requests, 'get', return_value=ResponseGetMock(200))
def test_mocked_store_response(mock_object, getfx, currency, date,
                               expected_result):
    getfx._get_response(currency, date)
    assert getfx._currency_code == expected_result[0]
    assert getfx._table_number == expected_result[1]
    assert getfx._effective_date == expected_result[2]
    assert getfx._rate == expected_result[3]
