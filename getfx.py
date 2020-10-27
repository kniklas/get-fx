import requests
import argparse


NBP_API = "http://api.nbp.pl/api/exchangerates/rates/A"
DEFAULT_CURRENCY = "CHF"


class GetFX(object):
    def __init__(self):
        self._currency_code = ""
        self._table_number = ""
        self._effective_date = ""
        self._rate = 0

    def _delete(self):
        "Garbage collection method."
        pass

    def _get_request_url(self):
        raise NotImplementedError

    def _store_response(self):
        raise NotImplementedError

    def __str__(self):
        return "Currency\t: {}\nTable number\t: {} \
                \nDate\t\t: {}\nFX rate\t\t: {}".format(
                    self._currency_code, self._table_number,
                    self._effective_date, self._rate)


class GetFxNBP(GetFX):
    def __init__(self, currency=DEFAULT_CURRENCY, date=None):
        super().__init__()
        self._get_response(currency, date)

    def _delete(self):
        print("--Teardown--")

    def _get_request_url(self, currency, date):
        "NBP API specific implementation of request URL composition."
        if date:
            url = '/'.join([NBP_API, currency, date])
        else:
            url = '/'.join([NBP_API, currency])
        return url

    def _store_response(self, resp):
        "NBP API specific implementation of storing JSON response."
        api_resp = resp.json()['rates'][0]
        self._table_number = api_resp['no']
        self._effective_date = api_resp['effectiveDate']
        self._rate = api_resp['mid']
        self._currency_code = resp.json()['code']

    def _get_response(self, currency, date=None):
        "NBP API specific implementation of requesting JSON response."
        resp = requests.get(self._get_request_url(currency, date))
        if resp.status_code == 404:
            raise Exception("Incorrect currency code: {} or date: {}"
                            .format(currency, date))
        self._store_response(resp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
GetFx : Copyright (c) 2020 Kamil Niklasiński
Program to display currency exchange rate.
""", formatter_class=argparse.RawTextHelpFormatter, epilog="""
Please note this program comes without any warranty!""")
    parser.add_argument('currency', metavar='CCY', type=str, nargs='?',
                        default=DEFAULT_CURRENCY,
                        help='Currency to get average NBP FX rate')
    parser.add_argument('-d', '--date',
                        help='effective currency exchange date')
    args = parser.parse_args()

    getfx = GetFxNBP(args.currency, date=args.date)
    print(getfx)
