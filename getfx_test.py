import pytest
from getfx import GetFx
# TODO: apply mock for connection, handle date as parameter


@pytest.fixture
def getfx():
    getfx = GetFx()
    yield getfx  # use generator to perform teardown
    getfx.delete()


def test_getfx_initialization(getfx):
    assert getfx


@pytest.mark.parametrize("currency, expected_url", (
    ("CHF", "http://api.nbp.pl/api/exchangerates/rates/A/CHF"),
    ("EUR", "http://api.nbp.pl/api/exchangerates/rates/A/EUR"),
    ("USD", "http://api.nbp.pl/api/exchangerates/rates/A/USD")
 ))
def test_URL_for_currency(getfx, currency, expected_url):
    assert getfx.get_request_url(currency) == expected_url


@pytest.mark.parametrize("currency, expected", (
    ("CHF", 200),
    ("EUR", 200),
    ("USD", 200),
    ("", 404),
    ("a", 404),
    ("USDa", 404)
 ))
def test_URL_connection(getfx, currency, expected):
    assert getfx.get_raw_response(currency).status_code == expected


def test_URL_exception(getfx):
    with pytest.raises(Exception):
        getfx.get_response('a')
    assert getfx.json_resp == []
