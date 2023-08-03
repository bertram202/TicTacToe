import telebot
from telebot import types
import random

bot = telebot.TeleBot('5958728121:AAEZukX3ZNq5agYsTd4k2fOymElkVz7yJwc')

free_space = ["1", "2", "3",
              "4", "5", "6",
              "7", "8", "9"]

all_space = ["1", "2", "3",
             "4", "5", "6",
             "7", "8", "9"]

table = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]


def check_win(smth):
    global free_space
    a = smth[0] == smth[1] and smth[1] == smth[2]
    b = smth[3] == smth[4] and smth[4] == smth[5]
    c = smth[6] == smth[7] and smth[7] == smth[8]
    d = smth[0] == smth[3] and smth[3] == smth[6]
    e = smth[1] == smth[4] and smth[4] == smth[7]
    f = smth[2] == smth[5] and smth[5] == smth[8]
    g = smth[0] == smth[4] and smth[4] == smth[8]
    h = smth[2] == smth[4] and smth[4] == smth[6]
    if a or b or c or d or e or f or g or h:
        if a or d or g:
            if smth[0] == "x":
                message = "ты победил!"
            elif smth[0] == "o":
                message = "ты проиграл!"
        elif b or e:
            if smth[4] == "x":
                message = "ты победил!"
            elif smth[4] == "o":
                message = "ты проиграл!"
        elif c:
            if smth[6] == "x":
                message = "ты победил!"
            elif smth[6] == "o":
                message = "ты проиграл!"
        elif f or h:
            if smth[2] == "x":
                message = "ты победил!"
            elif smth[2] == "o":
                message = "ты проиграл!"
        else:
            return False

        return message
    else:
        return False
# ----------------------------------------------------------------


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👾 Играть")
    btn2 = types.KeyboardButton("💵 Поддержать")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот креcтиков-ноликов Лабизаби".format(
        message.from_user), reply_markup=markup)
# ----------------------------------------------------------------


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global table, free_space
    if message.text.lower() == "играть" or message.text.lower() == "👾 играть":
        table = ["1", "2", "3",
                 "4", "5", "6",
                 "7", "8", "9"]
        free_space = ["1", "2", "3",
                      "4", "5", "6",
                      "7", "8", "9"]
        bot.send_photo(message.chat.id, open('img.jpeg', 'rb'))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        btn5 = types.KeyboardButton("5")
        btn6 = types.KeyboardButton("6")
        btn7 = types.KeyboardButton("7")
        btn8 = types.KeyboardButton("8")
        btn9 = types.KeyboardButton("9")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(message.from_user.id,
                         "выбери номер", reply_markup=markup)
        bot.register_next_step_handler(message, get_int)
    elif message.text.lower() == "/help":
        bot.send_message(message.from_user.id, 'напиши "играть"')
    elif message.text.lower() == "поддержать" or message.text.lower() == "💵 поддержать":
        bot.send_message(
            message.from_user.id, "ты можешь поддержать проект, перечислив любую сумму по QR-коду или номеру телефона +79825428823")
        bot.send_photo(message.chat.id, open('oplata.jpg', 'rb'))
    else:
        bot.send_message(message.from_user.id,
                         "ай донт андерстенд ю, не думаешь написать /help ?")
# ----------------------------------------------------------------


def showStartButtons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👾 Играть")
    btn2 = types.KeyboardButton("💵 Поддержать")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Летс гоу?", reply_markup=markup)


def get_int(message):
    if len(free_space):
        if message.text in free_space and check_win(table) == False:
            bot.send_message(message.from_user.id,
                             "ты закрасил поле под номером " + message.text)
            table[int(message.text)-1] = "x"
            free_space.remove(message.text)
            if check_win(table) == False:
                try:
                    random_number = random.choice(free_space)
                    bot.send_message(message.from_user.id,
                                     "я закрасил поле под номером " + random_number)
                    free_space.remove(random_number)
                    table[int(random_number)-1] = "o"
                    if check_win(table) != False:
                        # *******************************************
                        bot.send_message(message.from_user.id,
                                         check_win(table))
                        showStartButtons(message)
                    else:
                        bot.register_next_step_handler(message, get_int)
                except:
                    # *******************************************
                    bot.send_message(message.from_user.id, "ничья")
                    showStartButtons(message)
            else:
                # *******************************************
                bot.send_message(message.from_user.id, check_win(table))
                showStartButtons(message)
        elif check_win(table) != False:
            # *******************************************
            bot.send_message(message.from_user.id, check_win(table))
            showStartButtons(message)
        elif message.text in all_space:
            bot.send_message(message.from_user.id, "поле уже закрашено")
            bot.register_next_step_handler(message, get_int)
        else:
            bot.send_message(message.from_user.id, "введи число от 1 до 9")
            bot.register_next_step_handler(message, get_int)
    elif check_win(table) != False:
        # *******************************************
        bot.send_message(message.from_user.id, check_win(table))
        showStartButtons(message)
    else:
        # *******************************************
        bot.send_message(message.from_user.id, "ничья")
        showStartButtons(message)

# ----------------------------------------------------------------


bot.infinity_polling()
