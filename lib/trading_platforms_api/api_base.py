class BaseApi:
    # TODO: Здесь надо прописать все методы какие будут нужны для взаимодействия с биржами

    def __init__(self, **kwargs):
        self.api_key = kwargs.get("api_key", None)
        self.api_secret = kwargs.get("api_secret", None)
        self.api_password = kwargs.get("api_password", None)
        self.debug = kwargs.get("debug", False)

    def get_currency(self, symbol):
        # TODO: Должно ретёрнить значение {"value": курс, "time": время}
        pass

    def place_trade(self, action, *args, **kwargs):
        match action:
            case 'sell':
                pass
            case 'buy':
                pass
            case _:
                raise ValueError(f"Given unknown action: {action}")
