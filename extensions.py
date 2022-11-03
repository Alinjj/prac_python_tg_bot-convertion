import requests
import json
from command import values


class APIException(Exception):
    pass

class converter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Валюты не нуждаются в переводе: {base}-{quote}')

        try:
            base_ticker = values[base]
        except KeyError:
            raise APIException(f'Ошибка в первой валюте {base}')

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIException(f'Ошибка во второй валюте {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество должно быть числом')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        result = json.loads(r.content)[values[quote]]
        result *= amount

        return result