import requests


NBP_API = "http://api.nbp.pl/api/exchangerates/rates/A/"
DEFAULT_CURRENCY = "CHF"


class GetFx(object):
    def __init__(self):
        self._json_resp = []

    def _get_request_url(self, currency=DEFAULT_CURRENCY):
        return NBP_API + currency

    def _delete(self):
        "Garbage collection method."
        pass

    def _get_raw_response(self, currency=DEFAULT_CURRENCY):
        return requests.get(self._get_request_url(currency))

    def _store_response(self):
        self._table_number = self._json_resp['no']
        self._effective_date = self._json_resp['effectiveDate']
        self._rate = self._json_resp['mid']

    def _get_response(self, currency=DEFAULT_CURRENCY):
        resp = self._get_raw_response(currency)
        if resp.status_code == 404:
            raise Exception("Incorrect currency code: ", currency)
        self._json_resp = resp.json()['rates'][0]
        self._currency_code = resp.json()['code']
        self._store_response()

    def get_today_rate(self, currency=DEFAULT_CURRENCY):
        self._get_response(currency)
        print("Currency\t:", self._currency_code)
        print("Table number\t:", self._table_number)
        print("Date\t\t:", self._effective_date)
        print("FX rate\t\t:", self._rate)


if __name__ == "__main__":
    print("Welcome to GetFX program!")
    getfx = GetFx()
    getfx.get_today_rate()
