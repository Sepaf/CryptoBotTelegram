import json
import telebot
import requests

TOKEN = '5684741324:AAGZVbgvVPpWp19Ci7jeGmzArMIJxVt7-Dk'

bot = telebot.TeleBot('5684741324:AAGZVbgvVPpWp19Ci7jeGmzArMIJxVt7-Dk')

keys ={'биткоин': 'BTS',
       'эфириум': 'ETH',
       'доллар': 'USD'
       }

class ConvertioException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base:str, amount: str):
        if quote == base:
            raise ConvertioException(f'Невозможно перевести одинаковые валюты {base}. ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertioException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertioException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertioException(f' Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base


@bot.message_handler(commands=['start','help'])
def help(message:telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n Увидить список доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertioException('Слишком много параметров.')

    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount)
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()