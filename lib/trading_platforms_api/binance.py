import ccxt
from .api_base import BaseApi


# TODO: Здесь по сути надо только переопределить метод __init__, чтобы инициализировать правильный класс ccxt
#  а методы по взаимодействию с api будут в классе BaseApi, т.к. ccxt позаботились и сделали все по кайфу
#  ну и все другие платформы добавить тож в эту папку

class Binance(BaseApi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = ccxt.binance(
            {
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'password': self.api_password
            }
        )
