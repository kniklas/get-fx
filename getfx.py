import requests
import argparse


NBP_API = "http://api.nbp.pl/api/exchangerates/rates/A"
DEFAULT_CURRENCY = "CHF"


class GetFx(object):
    def __init__(self):
        self._json_resp = []

    def _get_request_url(self, currency=DEFAULT_CURRENCY, date=None):
        if date:
            url = '/'.join([NBP_API, currency, date])
        else:
            url = '/'.join([NBP_API, currency])
        return url

    def _delete(self):
        "Garbage collection method."
        pass

    def _get_raw_response(self, currency=DEFAULT_CURRENCY, date=None):
        return requests.get(self._get_request_url(currency, date))

    def _store_response(self):
        self._table_number = self._json_resp['no']
        self._effective_date = self._json_resp['effectiveDate']
        self._rate = self._json_resp['mid']

    def _get_response(self, currency=DEFAULT_CURRENCY, date=None):
        resp = self._get_raw_response(currency, date)
        if resp.status_code == 404:
            raise Exception("Incorrect currency code: {} or date: {}"
                            .format(currency, date))
        self._json_resp = resp.json()['rates'][0]
        self._currency_code = resp.json()['code']
        self._store_response()

    def get_today_rate(self, currency=DEFAULT_CURRENCY, date=None):
        self._get_response(currency, date)
        print("Currency\t:", self._currency_code)
        print("Table number\t:", self._table_number)
        print("Date\t\t:", self._effective_date)
        print("FX rate\t\t:", self._rate)


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

    getfx = GetFx()
    getfx.get_today_rate(currency=args.currency, date=args.date)
