class BaseApi:
    # TODO: Здесь надо прописать все методы какие будут нужны для взаимодействия с биржами

    def __init__(self, api_key, api_secret, api_password, debug=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_password = api_password
        self.debug = debug

    def get_currency(self):
        pass

    def place_trade(self, action, *args, **kwargs):
        match action:
            case 'sell':
                pass
            case 'buy':
                pass
            case _:
                raise ValueError(f"Given unknown action: {action}")
