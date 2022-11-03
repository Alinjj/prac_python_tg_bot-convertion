import telebot
from command import TOKEN, values, menu, help
from extensions import APIException, converter

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def greeting(message):
    bot.reply_to(message, text='Приветствуем тебя,это бот для конвертации валют,прочитай инструкцию')
    bot.send_message(message.chat.id, help + '\n /menu')
@bot.message_handler(commands=['help','menu'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"И снова привет, {message.chat.username}")
    bot.send_message(message.chat.id, help + '\n /menu')
@bot.message_handler(commands=['menu'])
def bot_main_menu(message):
    bot.send_message(message.chat.id, menu)

@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, help + '\n /menu')

@bot.message_handler(commands=['help'])
def bot_help(message):
    bot.send_message(message.chat.id, help + '\n /menu')

@bot.message_handler(commands=['values'])
def bot_values(message):
    bot.send_message(message.chat.id, 'Все валюты:')
    for i in values:
        bot.send_message(message.chat.id, i + ' ' + values[i] )
    bot.send_message(message.chat.id, '/menu')

@bot.message_handler(content_types=['text'])
def bot_convert_result(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) != 3:
            raise APIException('Ошибка:Прочитайте инструкцию по использованию бота')

        base, quote, amount = val
        result = converter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка.\n {e}')
    else:
        text = f'{amount} {values[base]}({base}) в {values[quote]}({quote}) равно: {result}'
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "/menu")

bot.polling()

