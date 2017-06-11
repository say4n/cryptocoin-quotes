from coinmarketcap import CoinMarketCapAPI, update_interval
import rumps

# TODO - toggle states
__version__ = "1.0.1"


class CryptoCoinSBA(rumps.App):
    def __init__(self):
        super(CryptoCoinSBA, self).__init__(name="CryptoCoin Quotes", title='', icon="icons/main.png")
        self._api = CoinMarketCapAPI(currency="INR")
        self.menu = [["Crypto Currency", [rumps.MenuItem("Bitcoin",  callback=self.bitcoin),
                                         rumps.MenuItem("Ethereum", callback=self.ethereum),
                                         rumps.MenuItem("Ripple",   callback=self.ripple),
                                         rumps.MenuItem("Litecoin", callback=self.litecoin)]],
                     ["Conversion Currency", [rumps.MenuItem(currency, callback=self.change_currency) for currency in
                                   self._api.valid_currencies]],
                     rumps.MenuItem("About", callback=self.about)]
        self.cryptocurrency = None

    def change_currency(self, sender):
        # set currency
        chosen_currency = sender.title
        self._api.set_currency(chosen_currency)

        # update info if bitcoin was chosen!
        if self.cryptocurrency is not None:
            method_name = self.cryptocurrency.title.lower()
            try:
                method = getattr(self, method_name)
                print(f"Calling method : {method_name}")
                method(self.cryptocurrency)
                print(f"Currency set to : {self._api.get_currency()}")
            except AttributeError:
                raise NotImplementedError(f"{method_name} not implemented")

    def bitcoin(self, sender):
        self.cryptocurrency = sender
        self.title = "{:.2f} {}".format(self._api.get_quote(id="bitcoin"), self._api.get_currency())
        self.icon = "icons/Bitcoin@2x.png"

    def ethereum(self, sender):
        self.cryptocurrency = sender
        self.title = "{:.2f} {}".format(self._api.get_quote(id="ethereum"), self._api.get_currency())
        self.icon = "icons/Ethereum@2x.png"

    def ripple(self, sender):
        self.cryptocurrency = sender
        self.title = "{:.2f} {}".format(self._api.get_quote(id="ripple"), self._api.get_currency())
        self.icon = "icons/Ripple@2x.png"

    def litecoin(self, sender):
        self.cryptocurrency = sender
        self.title = "{:.2f} {}".format(self._api.get_quote(id="litecoin"), self._api.get_currency())
        self.icon = "icons/Litecoin@2x.png"

    @rumps.timer(update_interval)
    def update_quote(self, _):
        # keep fetching quote every `update_interval` seconds
        print("Fetching data ...")
        self._api.get_ticker()
        print("Done ✓")

        if not self._api.internet_available:
            print("No connection")
            self.icon = "icons/ic_error_outline_black@2x.png"
            self.title = "Connection Error"

            # Make all inactive
            for menuItem in self.menu.values():
                menuItem.state = 0
        else:
            print("Working connection")
            if not self._api.response_available():
                self.icon = "icons/main.png"
                self.title = "CryptoCoin Quotes"

    def about(self, sender) -> None:
        app_version = __version__
        message = u"Copyright © 2017, Sayan Goswami\nAll Rights Reserved\n\nv{}".format(app_version)
        rumps.alert(title="About", message=message, ok='Close')


if __name__ == "__main__":
    CryptoCoinSBA().run()
