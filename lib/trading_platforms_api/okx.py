import ccxt
from .api_base import BaseApi


class Okx(BaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = ccxt.okex(
            {
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'password': self.api_password
            }
        )
