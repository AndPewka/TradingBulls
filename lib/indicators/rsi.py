from talib import RSI as RSI_
from numpy import array

from lib.influxdb import Wrapper


class RSI:
    """
    Usage:
    rsi = RSI()
    all_values = rsi.calculate(service, symbol).all()
    last_value = rsi.calculate(service, symbol).last()
    last_value_with_custom_period_and_interval = rsi.calculate(
        service,
        symbol,
        interval=your_interval_in_minutes,
        period=your_period
    ).last()
    """
    def __init__(self):
        self.__influx = Wrapper()
        self.__values = None

    def last(self):
        return None if self.__values is None else self.__values[-1]

    def all(self):
        return self.__values

    def calculate(self, service, symbol, interval=5, period=14):
        t_range = (period + 1) * 10 * interval

        query = self.__influx.gen_query()\
            .range(t_range, unit="m")\
            .measurement("currency")\
            .filter(service=service, currency_pair=symbol, _field="close_price")\
            .group_by_time(interval)\
            .keep("_value", "_time")()

        result = self.__influx.query(query)
        rates = array(list(map(lambda res: res["_value"], result)))

        self.__values = RSI_(rates, period)
        return self
