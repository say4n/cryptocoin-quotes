import datetime
import requests
from requests.exceptions import RequestException

update_interval = 60 * 5  # 5 minutes


class CoinMarketCapAPI:
    def __init__(self, currency="USD"):
        # variables
        self._url = "https://api.coinmarketcap.com/v1/ticker/?limit=10&convert="
        self.valid_currencies = ["AUD", "BRL", "CAD", "CHF", "CNY", "EUR", "GBP", "HKD", "IDR", "INR", "JPY", "KRW",
                                 "MXN", "RUB", "USD"]
        self._currency = self._validate_currency(currency)
        self._last_update = None
        self._cached_response = None
        self.internet_available = False
        self.update_interval = update_interval
        # pre-fetch the quote
        self.get_ticker()

    def _validate_currency(self, currency):
        if currency in self.valid_currencies:
            return currency
        else:
            return "USD"

    def response_available(self):
        return self._cached_response is not None

    def _time_since_last_update(self):
        """Returns time since the last ticker update"""
        return (datetime.datetime.utcnow() - self._last_update).total_seconds() // 60

    def get_ticker(self):
        if (self._last_update is None) or (self._time_since_last_update() >= self.update_interval) \
                or self._cached_response is None:
            # First run
            # 'or'
            # Limits for the API
            # Please limit requests to no more than 10 per minute.
            # Endpoints update every 5 minutes.
            try:
                self._cached_response = requests.get(self._url + self._currency).json()
                self._last_update = datetime.datetime.utcnow()
                self.internet_available = True
            except (RequestException, ):
                if self._cached_response is None:
                    self.internet_available = False
                pass

    def get_quote(self, id="bitcoin"):
        if self._cached_response is None:
            # First fetch
            self.get_ticker()

        try:
            for quote in self._cached_response:
                if quote["id"] == id:
                    return float(quote[f"price_{self._currency.lower()}"])

        except TypeError as e:
            return e
        except KeyError:
            return float("nan")

    def get_currency(self):
        return self._currency

    def set_currency(self, currency):
        if self._currency != currency:
            print(f"Setting currency to {currency}")
            self._currency = currency
            self._cached_response = None
            self.get_ticker()
            print("Done")

if __name__ == "__main__":
    test = CoinMarketCapAPI(currency="INR")
    print(test.get_quote(id="bitcoin"))
