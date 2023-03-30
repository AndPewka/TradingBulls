from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException


class Binance:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api = Client(api_key, api_secret, testnet=True)

    def get_history(self, symbol, months=None, days=None, hours=None, minutes=None):
        if not any([months, days, hours, minutes]):
            raise ValueError("Interval must be set.")

        start_string = ""
        if months:
            start_string += f"{months} month{(months * 's')[:1]} "
        if days:
            start_string += f"{days} day{(days * 's')[:1]} "
        if hours:
            start_string += f"{hours} hour{(hours * 's')[:1]} "
        if minutes:
            start_string += f"{minutes} minute{(minutes * 's')[:1]} "
        start_string += "ago UTC"

        try:
            res = self.api.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_string)
        except BinanceAPIException as error:
            raise ValueError(f"Binance API error: {error}.")

        return self.parse_klines(res)

    @staticmethod
    def parse_klines(klines_list):
        return list(map(
            lambda res: {
                "time": datetime.fromtimestamp(res[0] / 1000),
                "open_price": float(res[1]),
                "min_price": float(res[2]),
                "max_price": float(res[3]),
                "close_price": float(res[4]),
                "vol": float(res[5]),
                "close_time": int(res[6] / 1000),
                "qa_vol": float(res[7]),
                "trades_count": int(res[8]),
                "tb_ba_vol": float(res[9]),
                "tb_qa_vol": float(res[10])
            },
            klines_list
        ))
