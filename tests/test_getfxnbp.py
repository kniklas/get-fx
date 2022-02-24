import requests
from unittest.mock import patch

import pytest
from getfx.getfxnbp import GetFxNBP
from getfx import getfxnbp


STANDARD_RESPONSE_LIST = ["CHF", "203/A/NBP/2020", "2020-10-16", 4.2571]


class ResponseGetMockBase(object):
    def __init__(self, code):
        self.status_code = code


class ResponseGetMockNoConnection(ResponseGetMockBase):
    def __init__(self, code):
        super().__init__(code)

    @staticmethod
    def json():
        raise requests.exceptions.ConnectionError


class ResponseGetMock(ResponseGetMockBase):
    def __init__(self, code):
        super().__init__(code)

    @staticmethod
    def json():
        json_response = {
            "table": "A",
            "currency": "frank szwajcarski",
            "code": "CHF",
            "rates": [
                {
                    "no": "203/A/NBP/2020",
                    "effectiveDate": "2020-10-16",
                    "mid": 4.2571,
                }
            ],
        }
        return json_response


@pytest.fixture(name="getfx")
@patch.object(requests, "get", return_value=ResponseGetMock(200))
def fixture_getfx(mock_object, request):
    getfx = GetFxNBP()
    # Below is added as yield as teardown does not work

    def fin():
        getfx._delete()

    request.addfinalizer(fin)
    return getfx


def test_getfx_initialization(getfx):
    assert getfx


@pytest.mark.parametrize(
    "currency, date, expected_url",
    (
        ("CHF", None, "http://api.nbp.pl/api/exchangerates/rates/A/CHF"),
        (
            "CHF",
            "2020-10-16",
            "http://api.nbp.pl/api/exchangerates/rates/A/CHF/2020-10-16",
        ),
        ("EUR", None, "http://api.nbp.pl/api/exchangerates/rates/A/EUR"),
        ("USD", None, "http://api.nbp.pl/api/exchangerates/rates/A/USD"),
    ),
)
def test_URL_for_date_and_currency(getfx, currency, date, expected_url):
    assert getfx._get_request_url(currency, date) == expected_url


@patch.object(requests, "get", return_value=ResponseGetMock(404))
def test_mocked_URL_exception(mock_object):
    with pytest.raises(ValueError):
        getfx = GetFxNBP("R")
        getfx._delete()
    assert mock_object


@patch.object(requests, "get", return_value=ResponseGetMockNoConnection(200))
def test_no_connection(mock_object):
    with pytest.raises(SystemExit) as wrapped_exit:
        getfx = GetFxNBP()
        getfx._delete()
    assert wrapped_exit.typename == "SystemExit"
    assert wrapped_exit.value.code == 1


def test_mocked_json(getfx):
    assert getfx._rate == 4.2571


@pytest.mark.parametrize(
    "currency, date, expected_result",
    (
        ("CHF", None, STANDARD_RESPONSE_LIST),
        ("CHF", "2020-10-16", STANDARD_RESPONSE_LIST),
    ),
)
@patch.object(requests, "get", return_value=ResponseGetMock(200))
def test_mocked_store_response(mock_object, currency, date, expected_result):
    getfx = GetFxNBP(currency, date)
    assert getfx._currency_code == expected_result[0]
    assert getfx._table_number == expected_result[1]
    assert getfx._effective_date == expected_result[2]
    assert getfx._rate == expected_result[3]
    getfx._delete()


@patch.object(requests, "get", return_value=ResponseGetMock(200))
def test_main(mock_object):
    with patch.object(getfxnbp.sys, "exit", return_value=0) as mock_cmd:
        getfxnbp.init_cmd()
    assert mock_cmd.called


@patch.object(requests, "get", return_value=ResponseGetMock(404))
def test_cmd_value_error(mock_object):
    with pytest.raises(SystemExit):
        getfxnbp.init_cmd(["US"])
    assert mock_object.called
