import requests
from unittest.mock import patch
import pytest
from getfx import GetFx
# TODO: handle date as parameter
# TODO: handle other status codes than 200 and 404


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


@pytest.mark.parametrize("currency, expected_url", (
    ("CHF", "http://api.nbp.pl/api/exchangerates/rates/A/CHF"),
    ("EUR", "http://api.nbp.pl/api/exchangerates/rates/A/EUR"),
    ("USD", "http://api.nbp.pl/api/exchangerates/rates/A/USD")
 ))
def test_URL_for_currency(getfx, currency, expected_url):
    assert getfx._get_request_url(currency) == expected_url


@patch.object(requests, 'get', return_value=ResponseGetMock(404))
def test_mocked_URL_exception(mock_object, getfx):
    with pytest.raises(Exception):
        getfx._get_response("R")
    assert mock_object


@patch.object(requests, 'get', return_value=ResponseGetMock(200))
def test_mocked_json(mock_object, getfx):
    getfx._get_response("CHF")
    assert getfx._json_resp['mid'] == 4.2571


@patch.object(requests, 'get', return_value=ResponseGetMock(200))
def test_mocked_store_response(mock_object, getfx):
    getfx._get_response("CHF")
    assert getfx._currency_code == "CHF"
    assert getfx._table_number == "203/A/NBP/2020"
    assert getfx._effective_date == "2020-10-16"
    assert getfx._rate == 4.2571
