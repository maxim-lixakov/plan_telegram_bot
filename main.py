import telebot
from telebot import types
import config
from collections import defaultdict
import json

bot = telebot.TeleBot(config.TOKEN)

state = ""
TYPE, INFO, DATE = range(3)
USER_STATE = defaultdict(lambda: TYPE)
CURRENT_INFO = []
DATA = {"run": {"2020-07-22": ["\u043d\u0430 \u0441\u0442\u0430\u0434\u0438\u043e\u043d\u0435\n\u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430 5 \u043a\u043c\n200, 400, 4*800, 400, 200 (\u043f\u043e 35\u0441 \u043d\u0430 200\u043c)\n\u0437\u0430\u043c\u0438\u043d\u043a\u0430 2 \u043a\u043c"], "2020-07-23": ["\u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430 2 \u043a\u043c\n8 \u043a\u043c \u0432 \u0442\u0435\u043c\u043f\u0435 3:40"], "2020-07-24": ["\u043d\u0430 \u0441\u0442\u0430\u0434\u0438\u043e\u043d\u0435 \n\u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430 5 \u043a\u043c\n3*1200 (3.30, 3.36, 3.35)\n\u0431\u0435\u0433\u043e\u0432\u044b\u0435 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f \n\u0437\u0430\u043c\u0438\u043d\u043a\u0430 2 \u043a\u043c"], "2020-07-25": ["\u0432\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u0431\u0435\u0433 5 \u043a\u043c"], "2020-07-26": ["20 \u043a\u043c, \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0442\u0435\u043c\u043f 3.53 \n(4.00 \u043f\u0435\u0440\u0432\u0430\u044f \u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0430, 3.45 \u0432\u0442\u043e\u0440\u0430\u044f \u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0430)"], "2020-07-27": ["\u0441\u043f\u043e\u043a\u043e\u0439\u043d\u044b\u0439 \u043a\u0440\u043e\u0441\u0441 15 \u043a\u043c"], "2020-07-28": ["\u043d\u0430 \u0441\u0442\u0430\u0434\u0438\u043e\u043d\u0435 \n4 \u043a\u043c \u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430\n5*800 \u0441 \u043e\u0442\u0434\u044b\u0445\u043e\u043c ~ 3,5 \u043c\u0438\u043d\n(2:27, 2:22, 2:18, 2:20, 2:19)\n\u0431\u0435\u0433\u043e\u0432\u044b\u0435 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f\n1 \u043a\u043c \u0437\u0430\u043c\u0438\u043d\u043a\u0430"], "2020-07-29": ["10 \u043a\u043c \u0432\u043e\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043a\u0440\u043e\u0441\u0441"], "2020-07-30": ["\u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430 + \u0431\u0435\u0433\u043e\u0432\u044b\u0435 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f \n7 \u043a\u043c \u043f\u043e \u0434\u043e\u0440\u043e\u0433\u0435 \u0441 \u0442\u0435\u043c\u043f\u043e\u043c 3:40"], "2020-07-31": ["\u043e\u0442\u0434\u044b\u0445"], "2020-08-01": ["\u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430 2 \u043a\u043c\n5* (1 \u043c\u0438\u043d \u0431\u044b\u0441\u0442\u0440\u043e \u0447\u0435\u0440\u0435\u0437 4 \u043c\u0438\u043d \u0441\u043f\u043e\u043a\u043e\u0439\u043d\u043e\u0433\u043e \u0431\u0435\u0433\u0430)"], "2020-08-02": ["8 \u043a\u043c \u0431\u0435\u0433 \u0432 \u0441\u0440\u0435\u0434\u043d\u0435\u043c \u0442\u0435\u043c\u043f\u0435 (\u043f\u0440\u0438\u043c\u0435\u0440\u043d\u043e 4:00)"]}, "swim": {"2020-07-31": ["\u0441\u0438\u043b\u043e\u0432\u0430\u044f\n400 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441 + 200 \u0432\u0441\n800 \u0440\u0435\u0437\u0438\u043d\u0430\n3 \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u044f * 25\u043c\n800 \u0440\u0443\u043a\u0438\n2 \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u044f * 25\u043c\n800 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441"], "2020-08-01": ["600 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0441 + 200 \u0443\u043f\u0440\u0430\u0436\u043d\u0435\u043d\u0438\u044f \n\u0440\u0430\u0431\u043e\u0442\u0430 3*(6*100)  \n\u043f\u0435\u0440\u0432\u0430\u044f \u0441\u0435\u0440\u0438\u044f \u043f\u043e 1:15 \u0441 \u0440\u0435\u0436\u0438\u043c\u043e\u043c 1:30\n\u0432\u0442\u043e\u0440\u0430\u044f \u0441\u0435\u0440\u0438\u044f \u043f\u043e 1:13 \u0441 \u0440\u0435\u0436\u0438\u043c\u043e\u043c 1:35\n\u0442\u0440\u0435\u0442\u044c\u044f \u0441\u0435\u0440\u0438\u044f \u043f\u043e 1:11 \u0441 \u0440\u0435\u0436\u0438\u043c\u043e\u043c 1:40\n400 \u0437\u0430\u043a\u0443\u043f\u043a\u0430"]}, "bike": {"2020-07-31": ["40 \u043c\u0438\u043d\u0443\u0442 \u0440\u0430\u0437\u043c\u0438\u043d\u043a\u0430 \u043f\u043e \u0432\u0435\u0440\u0445\u0443\n2 \u043a\u0440\u0443\u0433\u0430 \u043d\u0430 \u0441\u043a\u043e\u0440\u043e\u0441\u0442\u044c (7:10, 7:05)\n1 \u043a\u0440\u0443\u0433 \u0437\u0430\u043a\u0430\u0442\u043a\u0430"], "2020-08-01": ["\u0432\u0435\u043b\u043e 1,5\u0447 - 10 \u043a\u0440\u0443\u0433\u043e\u0432 (\u043f\u0440\u0438\u043c\u0435\u0440\u043d\u043e \u043f\u043e 9:00)"], "2020-08-02": ["\u0434\u043b\u0438\u043d\u043d\u0430\u044f \u0442\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430: 60 \u043a\u043c - 2 \u0447\u0430\u0441\u0430 ( \u043f\u043e 20 \u043c\u0438\u043d \u043d\u0430 \u043a\u0440\u0443\u0433 10\u043a\u043c)"]}}


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state_):
    USER_STATE[message.chat.id] = state_


def create_keyboard(list_):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=a, callback_data=a) for a in list_]
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(func=lambda message: get_state(message) == TYPE)
def start_command(message):
    if message.chat.id == 608433722:
        keyboard = create_keyboard(["run", "bike", "swim"])
        bot.send_message(
            message.chat.id,
            "записать тренировку",
            reply_markup=keyboard,
        )
    keyboard = create_keyboard(["бег", "вело", "плавание"])
    bot.send_message(
        message.chat.id,
        "выбрать вид",
        reply_markup=keyboard,
    )


@bot.message_handler(func=lambda message: get_state(message) == DATE)
def date_command(message):
    CURRENT_INFO.append(message.text)
    bot.send_message(message.chat.id, "запись тренировки")
    update_state(message, INFO)


@bot.message_handler(func=lambda message: get_state(message) == INFO)
def second_command(message):
    global CURRENT_INFO
    CURRENT_INFO.append(message.text)
    DATA[CURRENT_INFO[0]][CURRENT_INFO[1]] = [CURRENT_INFO[2]]
    update_state(message, TYPE)
    CURRENT_INFO = []
    bot.send_message(message.chat.id, "тренировка записана")
    with open("my_plan.json", "w") as write_file:
        json.dump(DATA, write_file)
    start_command(message)


@bot.callback_query_handler(func=lambda x: True)
def callback_query(callback_query_):
    global state
    message = callback_query_.message
    text = callback_query_.data
    if text == "run":
        update_state(message, INFO)
        CURRENT_INFO.append("run")
        keyboard = create_keyboard(["указать дату"])
        bot.send_message(message.chat.id, "дата", reply_markup=keyboard)
    if text == "bike":
        update_state(message, INFO)
        CURRENT_INFO.append("bike")
        keyboard = create_keyboard(["указать дату"])
        bot.send_message(message.chat.id, "дата", reply_markup=keyboard)
    if text == "swim":
        update_state(message, INFO)
        CURRENT_INFO.append("swim")
        keyboard = create_keyboard(["указать дату"])
        bot.send_message(message.chat.id, "дата", reply_markup=keyboard)
    if text == "бег":
        keyboard = create_keyboard(list(DATA["run"].keys()))
        bot.send_message(message.chat.id, "выбрать дату", reply_markup=keyboard)
        state = "run"
    if text == "плавание":
        keyboard = create_keyboard(list(DATA["swim"].keys()))
        bot.send_message(message.chat.id, "выбрать дату", reply_markup=keyboard)
        state = "swim"
    if text == "вело":
        keyboard = create_keyboard(list(DATA["bike"].keys()))
        bot.send_message(message.chat.id, "выбрать дату", reply_markup=keyboard)
        state = "bike"
    if text == "указать дату":
        update_state(message, DATE)
        bot.send_message(message.chat.id, "ввести дату")
    try:
        if text[:4] == "2020" and state == "run":
            bot.send_message(message.chat.id, DATA["run"][text])
        if text[:4] == "2020" and state == "swim":
            bot.send_message(message.chat.id, DATA["swim"][text])
        if text[:4] == "2020" and state == "bike":
            bot.send_message(message.chat.id, DATA["bike"][text])
    except KeyError:
        if state == "run":
            staterus = "бег"
        elif state == "swim":
            staterus = "плавание"
        else:
            staterus = "вело"
        bot.send_message(message.chat.id, f'в выбраном режиме: {staterus}\n'
                                          f'дата: {text} отствует, необходимо выбать другой режим в меню ')


bot.polling(none_stop=True)

