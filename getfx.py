import requests


NBP_API = "http://api.nbp.pl/api/exchangerates/rates/A/"
DEFAULT_CURRENCY = "CHF"


class GetFx(object):
    def __init__(self):
        self.json_resp = []

    def get_request_url(self, currency=DEFAULT_CURRENCY):
        self.request_url = NBP_API + currency
        return NBP_API + currency

    def delete(self):
        "Garbage collection method."
        pass

    def get_response(self, currency=DEFAULT_CURRENCY):
        resp = self.get_raw_response(currency)
        if resp.status_code == 404:
            raise Exception("Incorrect currency code: ", currency)
        self.json_resp = resp.json()['rates'][0]
        self.store_response()

    def get_raw_response(self, currency=DEFAULT_CURRENCY):
        return requests.get(self.get_request_url(currency))

    def store_response(self):
        self.table_number = self.json_resp['no']
        self.effective_date = self.json_resp['effectiveDate']
        self.rate = self.json_resp['mid']

    #  def get_today_rate(currency=DEFAULT_CURRENCY):
    #      response = requests.get(get_url(currency)).json()['rates'][0]
    #      print("Table number\t:", response['no'])
    #      print("Date\t\t:", response['effectiveDate'])
    #      print("FX rate\t\t:", response['mid'])


if __name__ == "__main__":
    print("Welcome to GetFX program!")
#  get_today_rate("CHF")
