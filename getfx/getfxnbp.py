"""Module implements NBP specific API to retrieve FX rates.

Module provides NBP API class: `GetFXNBP` which implements specific methods to
retrieve FX rates. It uses module variables:
- `NBP_API_URL` -- specifies URL for NBP API web service

It depends on importing `DEFAULT_CURRENCY` from `cmdparser` modules to define
which currency to use if it is not provided and on `parse_getfx()` method to
parse commandline arguments.
"""

import requests
import sys

try:
    # Below is implemented only for unit tests to pass
    from getfx.cmdparser import DEFAULT_CURRENCY, parse_getfx
    from getfx.getfx import GetFX
except ImportError:
    # Below is required if run from command line
    # NOTE: below is not unit tested might be not required if package is used
    from cmdparser import DEFAULT_CURRENCY, parse_getfx
    from getfx import GetFX

NBP_API_URL = "http://api.nbp.pl/api/exchangerates/rates/A"


def init_cmd(test_args=None):
    """Parse command line attributes and create GetFXNBP instance.

    It uses `parse_args` method from `cmdparser` module to parse commandline
    attributes. It creates instance of `GetFXNBP` object to handle request and
    response from NBP API.

    Raises SystemExit exception if incorrect attributes are used. Returned exit
    codes:
        0: no errors
        1: no connection (see `_get_response()` method)
        2: incorrect date or currency parameter
    """
    args = parse_getfx(test_args)
    try:
        getfx = GetFxNBP(args.currency, date=args.date)
        print(getfx)
        sys.exit(0)
    except ValueError:
        print("Wrong currency or date. Use \'-h\' option to display help.")
        raise SystemExit(2)


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
        """Receive JSON response from FX provider.

        Raises ValueError execption if incorrect parameters are used.
        Exit and return exit code = 1 if no internet connection is found.
        """
        try:
            resp = requests.get(self._get_request_url(currency, date))
            self._store_response(resp)
        except requests.exceptions.ConnectionError:
            print("No connection to NBP API!")
            sys.exit(1)
        else:
            if resp.status_code == 404:
                raise ValueError("Incorrect currency code: {} or date: {}"
                                 .format(currency, date))
