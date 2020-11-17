import pytest
from getfx.getfx import GetFX


@pytest.fixture(name='getfx2')
def fixture_getfx():
    getfx = GetFX()
    yield getfx
    getfx._delete()


def test_getfx_initialization(getfx2):
    assert getfx2


def test_initialization_attributes(getfx2):
    assert getfx2._currency_code == ""
    assert getfx2._table_number == ""
    assert getfx2._effective_date == ""
    assert getfx2._rate == 0


def test_not_implemented_methods(getfx2):
    with pytest.raises(NotImplementedError):
        getfx2._get_request_url()
    with pytest.raises(NotImplementedError):
        getfx2._store_response()


def test_str_returns_str(getfx2):
    assert type(getfx2.__str__()) == str
