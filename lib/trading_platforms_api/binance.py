from binance.client import Client


class Binance:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api = Client(api_key, api_secret, testnet=True)

    def get_currency(self, symbol):
        return self.api.futures_symbol_ticker(symbol=symbol)

    def get_klines(self, symbol, interval, limit=500):
        return self.api.futures_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
