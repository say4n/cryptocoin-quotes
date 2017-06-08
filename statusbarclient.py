from coinmarketcap import CoinMarketCapAPI
from coinmarketcap import update_interval
import rumps

# TODO - Add currency chooser


class CryptoCoinSBA(rumps.App):
    def __init__(self):
        super(CryptoCoinSBA, self).__init__(name="CryptoCoin Quotes", title="CryptoCoin Quotes", icon="icons/main.png")
        self._api = CoinMarketCapAPI(currency="INR")
        self.menu = ["Bitcoin", "Ethereum", "Litecoin", "Ripple"]

    @rumps.clicked("Bitcoin")
    def bitcoin(self, sender):
        self.title = "{:.2f} INR".format(self._api.get_quote(id="bitcoin"))
        self.icon = "icons/Bitcoin@2x.png"
        sender.state = 1
        self._toggle_states(sender)

    @rumps.clicked("Ethereum")
    def ether(self, sender):
        self.title = "{:.2f} INR".format(self._api.get_quote(id="ethereum"))
        self.icon = "icons/Ethereum@2x.png"
        sender.state = 1
        self._toggle_states(sender)

    @rumps.clicked("Ripple")
    def ripple(self, sender):
        self.title = "{:.2f} INR".format(self._api.get_quote(id="ripple"))
        self.icon = "icons/Ripple@2x.png"
        sender.state = 1
        self._toggle_states(sender)

    @rumps.clicked("Litecoin")
    def litecoin(self, sender):
        self.title = "{:.2f} INR".format(self._api.get_quote(id="litecoin"))
        self.icon = "icons/Litecoin@2x.png"
        sender.state = 1
        self._toggle_states(sender)

    def _toggle_states(self, sender):
        # switch off all other states
        for menuItem in self.menu.values():
            if menuItem.title not in [sender.title, "Quit"]:
                menuItem.state = 0

        # for debugging
        # for menuItem in self.menu.values():
        #     print(f"{menuItem.title} - {menuItem.state}")

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
            self.icon = "icons/main.png"
            self.title = "CryptoCoin Quotes"


if __name__ == "__main__":
    CryptoCoinSBA().run()
