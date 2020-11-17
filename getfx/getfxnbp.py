"""Module implements NBP specific API to retrieve FX rates.

Module provides NBP API class: `GetFXNBP` which implements specific methods to
retrieve FX rates. It uses module variables:
- `NBP_API_URL` -- specifies URL for NBP API web service

It depends on importing `DEFAULT_CURRENCY` from `parser` modules to define
which currency to use if it is not provided.
"""

import requests

from getfx import GetFX
try:
    from parser import DEFAULT_CURRENCY
except ImportError:
    # Below is implemented only for unit tests to pass
    from getfx.parser import DEFAULT_CURRENCY

NBP_API_URL = "http://api.nbp.pl/api/exchangerates/rates/A"


class GetFxNBP(GetFX):
    """Subclass of `GetFX` class to implement NBP specific FX retrieval logic.

    It does not provide public methods, instead it is assumed when instance is
    created, NBP API is invoked and FX rate retrieved. Access to retrieved rate
    is achieved via printing the instance using overriden: `__str__()` method.
    """

    def __init__(self, currency=DEFAULT_CURRENCY, date=None):
        """Set-up instance attributes and invoke FX request."""
        super().__init__()
        self._get_response(currency, date)

    def _delete(self):
        """Print object teardown message for debugging only."""
        print("--Teardown--")

    def _get_request_url(self, currency, date):
        """Return request URL for NBP API."""
        if date:
            url = '/'.join([NBP_API_URL, currency, date])
        else:
            url = '/'.join([NBP_API_URL, currency])
        return url

    def _store_response(self, resp):
        """Store reponse in instance attributes from received JSON."""
        api_resp = resp.json()['rates'][0]
        self._table_number = api_resp['no']
        self._effective_date = api_resp['effectiveDate']
        self._rate = api_resp['mid']
        self._currency_code = resp.json()['code']

    def _get_response(self, currency, date=None):
        """Receive JSON response from FX provider."""
        resp = requests.get(self._get_request_url(currency, date))
        if resp.status_code == 404:
            raise Exception("Incorrect currency code: {} or date: {}"
                            .format(currency, date))
        self._store_response(resp)
