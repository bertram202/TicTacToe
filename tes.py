import telebot
from telebot import types # для указание типов

bot = telebot.TeleBot('5976836873:AAFFf7zsE85-1b3N1_EN1upPCKOc38VrFKI') # токен лежит в файле config.py
markup = types.InlineKeyboardMarkup()

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    global markup
    button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
    button2 = types.InlineKeyboardButton("Сайт Хбр", url='https://habr.com/ru/all/')
    button3 = types.InlineKeyboardButton("Сайт Хр", url='https://habr.com/ru/all/')
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user), reply_markup=markup)

bot.polling(none_stop=True)