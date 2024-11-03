import telebot
from telebot import types

bot = telebot.TeleBot('5976836873:AAFxjqCqpLcXUslTB786Sgyxf5JmDnMkwTw')

free_space = ["1", "2", "3",
              "4", "5", "6",
              "7", "8", "9"]

occupied_space = ["1", "2", "3",
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
                return player1_link
            elif smth[0] == "o":
                return player2_link
        elif b or e:
            if smth[4] == "x":
                return player1_link
            elif smth[4] == "o":
                return player2_link
        elif c:
            if smth[6] == "x":
                return player1_link
            elif smth[6] == "o":
                return player2_link
        elif f or h:
            if smth[2] == "x":
                return player1_link
            elif smth[2] == "o":
                return player2_link
        else:
            return False
    else:
        return False
# ----------------------------------------------------------------

bot.set_my_commands([
    telebot.types.BotCommand("/play", "👾 Играть"),
    telebot.types.BotCommand("/donate", "💵 Поддержать"),
    telebot.types.BotCommand("/help", "❓ Помощь")
])

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👾 Играть")
    btn2 = types.KeyboardButton("💵 Поддержать")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Здарова! Я бот креcтиков-ноликов Лабизаби".format(
        message.from_user), reply_markup=markup)
# ----------------------------------------------------------------


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global table, free_space, player1, player2, occupied_space, player1_link, player2_link, firstPlayersStep
    if message.text.lower() == "/play" or message.text.lower() == "/play@labizabi_bot":
        table = ["1", "2", "3",
                 "4", "5", "6",
                 "7", "8", "9"]
        free_space = ["1", "2", "3",
                      "4", "5", "6",
                      "7", "8", "9"]
        occupied_space = ["1", "2", "3",
              "4", "5", "6",
              "7", "8", "9"]
        player2 = ""
        firstPlayersStep = True
        player1 = message.from_user.first_name
        player2_link = ""
        player1_link = "[{0}](https://t.me/{1})".format(player1, message.from_user.username)
        bot.send_photo(message.chat.id, open('img.jpeg', 'rb'))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #начало
        i = 1
        while i < 9:
            btn = types.KeyboardButton(str(i))
            btn2 = types.KeyboardButton(str(i+1))
            btn3 = types.KeyboardButton(str(i+2))
            markup.add(btn, btn2, btn3)
            i += 3
        #конец
        bot.send_message(message.chat.id,
                         "выбери номер", reply_markup=markup)
        if firstPlayersStep:
            bot.register_next_step_handler(message, get_int)
        else:
            bot.register_next_step_handler(message, get_int2)
    elif message.text.lower() == "/help" or message.text.lower() == "/help@labizabi_bot":
        bot.send_message(message.chat.id, 'напиши /play пж')
    elif message.text.lower() == "/donate" or message.text.lower() == "/donate@labizabi_bot":
        bot.send_message(
            message.chat.id, "вы можете поддержать проект и его автора, перечислив любую сумму по QR-коду или номеру телефона +79825428823")
        bot.send_photo(message.chat.id, open('oplata.jpg', 'rb'))
# ----------------------------------------------------------------


def showStartButtons(message):
    if len(free_space):
        bot.send_message(message.chat.id, "{0} победил".format(check_win(table)), parse_mode='MarkdownV2', disable_web_page_preview=True)
        ##bot.send_message(message.chat.id, "{0}, твой ".format(player2_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
    markup = types.ReplyKeyboardRemove()
    #btn1 = types.KeyboardButton("👾 Играть")
    #btn2 = types.KeyboardButton("💵 Поддержать")
    #markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Летс гоу?", reply_markup=markup)

def replaceButton(number, text, player, message):
    global occupied_space
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    occupied_space[number-1] = text
    i = 0
    while i < 9:
        btn = types.KeyboardButton(occupied_space[i])
        btn2 = types.KeyboardButton(occupied_space[i+1])
        btn3 = types.KeyboardButton(occupied_space[i+2])
        markup.add(btn, btn2, btn3)
        i += 3
    bot.send_message(message.chat.id,
                             "игрок {0} закрасил поле под номером ".format(player) + message.text, reply_markup=markup, parse_mode='MarkdownV2', disable_web_page_preview=True)

def get_int(message):
    global player2, player1, firstPlayersStep, player2_link
    name = message.from_user.first_name
    if name != player1 and player2 == "":
        player2 = name
        player2_link = "[{0}](https://t.me/{1})".format(player2 ,message.from_user.username)
    if len(free_space) and name == player1: #если есть свободные места и отправитель игрок номер 1
        if message.text in free_space and check_win(table) == False and name == player1:
            replaceButton(int(message.text), "❌", player1_link, message)
            table[int(message.text)-1] = "x"
            free_space.remove(message.text)
            if check_win(table) == False:
                if len(free_space) == False:
                    bot.send_message(message.chat.id, "ничья")
                    showStartButtons(message) 
                else:
                    if player2 != "":
                        bot.send_message(message.chat.id, "{0}, твой ход".format(player2_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
                    firstPlayersStep = False
                    bot.register_next_step_handler(message, get_int2)
            else:
                # *******************************************
                showStartButtons(message)
            #игрок 1 ходи
        elif check_win(table) != False:
            # *******************************************
            showStartButtons(message)
        elif message.text in all_space:
            bot.send_message(message.chat.id, "{0}, поле уже закрашено".format(player1_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
            bot.register_next_step_handler(message, get_int)
        else:
            bot.send_message(message.chat.id, "{0}, введи число от 1 до 9".format(player1_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
            bot.register_next_step_handler(message, get_int)
    elif check_win(table) != False:
        # *******************************************
        showStartButtons(message)
    elif len(free_space) == False:
        # *******************************************
        bot.send_message(message.chat.id, "ничья")
        showStartButtons(message)
    else:
        bot.register_next_step_handler(message, get_int)


def get_int2(message):
    global player2, player1, firstPlayersStep, player2_link
    name = message.from_user.first_name
    if name != player1 and player2 == "":
        player2 = name
        player2_link = "[{0}](https://t.me/{1})".format(player2, message.from_user.username)
    if len(free_space) and name == player2:
        if message.text in free_space and check_win(table) == False and name == player2:
            replaceButton(int(message.text), "⭕️", player2_link, message)
            table[int(message.text)-1] = "o"
            free_space.remove(message.text)
            if check_win(table) == False:
                if len(free_space) == False:
                    bot.send_message(message.chat.id, "ничья")
                    showStartButtons(message) 
                else:
                    firstPlayersStep = True
                    bot.send_message(message.chat.id, "{0}, твой ход".format(player1_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
                    bot.register_next_step_handler(message, get_int)
            else:
                # *******************************************
                showStartButtons(message)
            #игрок 2 ходи
        elif check_win(table) != False:
            # *******************************************
            showStartButtons(message)
        elif message.text in all_space:
            bot.send_message(message.chat.id, "{0}, поле уже закрашено".format(player2_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
            bot.register_next_step_handler(message, get_int2)
        else:
            bot.send_message(message.chat.id, "{0}, введи число от 1 до 9".format(player2_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
            bot.register_next_step_handler(message, get_int2)
    elif check_win(table) != False:
        # *******************************************
        showStartButtons(message)
    elif len(free_space) == False:
        # *******************************************
        bot.send_message(message.chat.id, "ничья")
        showStartButtons(message)
    else:
        bot.register_next_step_handler(message, get_int2)
# ----------------------------------------------------------------

bot.infinity_polling()
