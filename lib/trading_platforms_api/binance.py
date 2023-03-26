from .api_base import BaseApi
from binance.client import Client

class Binance(BaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.api = Client(self.api_key, self.api_secret, testnet=True)

    def get_current_currency(self, sybmol):
        return self.api.futures_symbol_ticker(symbol=sybmol)
    
    def get_klines(self, symbol, interval, limit=500):
        return self.api.futures_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
