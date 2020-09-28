import telebot
from telebot import types
from collections import defaultdict
import json


with open("file_name", "r") as f:
    DATA = json.load(f)


status = ["", ""]
state = ""
TOKEN = "1300872028:AAFZCKxpZM96IoK_R6cfS8MLp09tVmMX8Y8"
TYPE, INFO, DATE = range(3)
USER_STATE = defaultdict(lambda: TYPE)
CURRENT_INFO = []
months_list = ["январь", "февраль", "март",
               "апрель", "май", "июнь",
               "июль", "август", "сентябрь",
               "октябрь", "ноябрь", "декабрь"]
months = {"01": "январь", "02": "февраль", "03": "март",
          "04": "апрель", "05": "май", "06": "июнь",
          "07": "июль", "08": "август", "09": "сентябрь",
          "10": "октябрь", "11": "ноябрь", "12": "декабрь"}
run_dates = {}
for key in DATA["run"]:
    if key[:4] in run_dates:
        if months[key[5:7]] in run_dates[key[:4]]:
            run_dates[key[:4]][months[key[5:7]]].append(key[8:10])
        else:
            run_dates[key[:4]].update({months[key[5:7]]: [key[8:10]]})
    else:
        run_dates[key[:4]] = {months[key[5:7]]: []}
        run_dates[key[:4]][months[key[5:7]]].append(key[8:10])


bot = telebot.TeleBot(TOKEN)


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
            f"записать тренировку",
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
    if message.text[:4] == "2020":
        CURRENT_INFO.append(message.text)
        bot.send_message(message.chat.id, "запись тренировки")
        update_state(message, INFO)
    else:
        bot.send_message(message.chat.id, "некорректная дата")


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
    global state, status
    message = callback_query_.message
    text = callback_query_.data
    if message.chat.id == 608433722:
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
        keyboard = create_keyboard(list(run_dates.keys()))
        bot.send_message(message.chat.id, "выберитие год: ", reply_markup=keyboard)
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
            keyboard = create_keyboard(run_dates[text].keys())
            bot.send_message(message.chat.id, "выберите месяц: ", reply_markup=keyboard)
            status = [text]
        if text[:4] == "2020" and state == "swim":
            bot.send_message(message.chat.id, DATA["swim"][text])
        if text[:4] == "2020" and state == "bike":
            bot.send_message(message.chat.id, DATA["bike"][text])
        if text in months_list:
            keyboard = create_keyboard(run_dates[status[0]][text])
            bot.send_message(message.chat.id, "выберите день: ", reply_markup=keyboard)
            status.append(text)
        elif len(text) == 2:
            date = ""
            for number in months:
                if months[number] == status[1]:
                    date = status[0] + "-" + number + "-" + text
                    break
            bot.send_message(message.chat.id, DATA["run"][date])
            status = ["", ""]
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

