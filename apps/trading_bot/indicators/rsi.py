import numpy as np
import talib
from apps.telegram_bot.models import Rsi


class RSI:
    def __init__(self, client, symbol, interval, period=3, infelicity=3):
        self.client = client
        self.symbol = symbol
        self.interval = interval
        self.period = period
        self.infelicity = infelicity
        self.side = ""
        self.value = self.get_value()
        self.last_value = self.value
        self.price = self.get_value()
    
    def get_value(self):
        klines = self.client.get_klines(symbol=self.symbol, interval=self.interval)
        close_prices = np.array([float(kline[4]) for kline in klines])
        return talib.RSI(close_prices, self.period)[-1]
    
    def update_status(self):
        self.last_value = self.value
        self.value = self.get_value()

        Rsi.objects.create(symbol=self.symbol,
                            interval=self.interval,
                            period=self.period,
                            infelicity=self.infelicity,
                            value=self.value,
                            side=self.side,
                            last_value=self.last_value,
                            price=0)
    
    def print_info(self):
        print("value: {}, last_value: {}".format(self.value, self.last_value))


# RSI logic
# interval
# period
# value
# last_value
# infelicity
# side (Short/long)
