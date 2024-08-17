import telebot

from config import TOKEN, keys
from utilts import Converter, ConverterInputExc, ConverterServerExc


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты> (через пробел)' \
           '\nЧтобы увидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f"\n  {key.capitalize()}"
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    mess = message.text

    # проверка на случай ввода несуществующей команды
    if mess[0] == "/":
        comm_lst = ['/start', '/help', '/values']
        if mess not in comm_lst:
            mess = mess.replace("/", "'/'")
            text = f"неизвестная команда: {mess}\nДоступные команды:"
            for comm in comm_lst:
                text += f"\n   {comm}"
            bot.reply_to(message, text)
    else:
        try:
            # замена слеша на '/' чтобы неправильно введенный текст не подсвечивался как гиперссылка
            mess = message.text.lower().replace("/", "'/'").split(' ')
            if len(mess) != 3:
                exc = f'Неправильное количество введенных параметров: {message.text}\nПравила ввода:/help'
                raise ConverterInputExc(exc)

            text = Converter.converter(mess)

        except ConverterInputExc as e:
            text = f'Ошибка пользователя:\n{e}'
            bot.reply_to(message, text)
        except ConverterServerExc as e:
            text = f'Ошибка на сервере:\n{e}'
            bot.reply_to(message, text)
        except Exception as e:
            text = f'Неучтенная ошибка бота:\n{e}'
            bot.reply_to(message, text)
        else:
            bot.send_message(message.chat.id, text)


bot.polling()
