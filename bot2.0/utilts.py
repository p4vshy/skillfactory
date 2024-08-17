
import requests
import json
from config import server, keys


class ConverterInputExc(Exception):
    pass


class ConverterServerExc(Exception):
    pass


class Converter:
    @staticmethod
    def converter(mess: list):
        # data = None
        # проверки ошибок с серверной части.
        try:
            status = requests.get(server).status_code
        except:
            raise ConverterServerExc('Неверный адрес сервера с которого запрашивается API')
        else:
            if str(status)[0] == '4':
                raise ConverterServerExc(f"Статус запроса: {status}")
            elif str(status)[0] == '5':
                raise ConverterServerExc(f"Нет ответа с сервера: {status}")

        # проверка возможности получения json.
        try:
            data = requests.get(server).json()
        except Exception as e:
            raise ConverterServerExc(f'Не удалось получить json\n{e}')
            
        currency_from, currency_to, amount_str = mess

        # если введены одинаковые валюты.
        if currency_from == currency_to:
            raise ConverterInputExc(f"Нельзя перевести {currency_from} в {currency_to}")

        # проверка количества переводимой валюты.
        try:
            amount = round(float(amount_str.replace(',', '.')), 4)  # если введена запятая вместо точки
        except ValueError:
            raise ConverterInputExc(f"Количество переводимой валюты введено неверно: {amount_str}")

        if amount < 0:
            raise ConverterInputExc(f"Количество переводимой валюты не должно быть отрицательным: {amount_str}")

        # проверка первой валюты
        if currency_from not in keys:
            raise ConverterInputExc(f"Переводимая валюта введена неверно или отсутствует: {currency_from}\n"
                                    f"Доступные валюты:/values")

        # проверка второй валюты
        if currency_to not in keys:
            raise ConverterInputExc(f"Валюта в которою переводят введена неверно или отсутствует: {currency_to}\n"
                                    f"Доступные валюты:/values")

        currency_from = keys[currency_from]  # присвоение аббревиатуры
        currency_to = keys[currency_to]  # присвоение аббревиатуры

        # создание переменных курса валют к рублю
        first_to_rub = data['Valute'][currency_from]['Value'] if currency_from != 'RUB' else 1
        second_to_rub = data['Valute'][currency_to]['Value'] if currency_to != 'RUB' else 1
        try:
            result = round((first_to_rub * amount / second_to_rub), 2)
        except ZeroDivisionError:
            raise ConverterServerExc(f"Произошло деление на 0\nвалюта_1={first_to_rub}, валюта_2={second_to_rub}")
        text = f'{amount} {currency_from} = {result} {currency_to}'
        return text
