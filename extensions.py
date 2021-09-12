import requests
import json
from configuration import keys

class ConversionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}')

        if amount < 0:
            myError = ValueError(f'Введено отрицательное число переводимой валюты {amount}')
            raise myError

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym='f'{quote_ticker}&tsyms={base_ticker}')
        current_rate = json.loads(r.content)[keys[base]]
        total_base = round(current_rate * amount, 2)

        return total_base