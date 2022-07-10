
# -*- coding: utf-8 -*-
import csv
import sys
import time
import rosapi
import telebot
import schedule
import threading
from telebot import types
from functools import wraps
from rosapi import add_user
from rosapi import remove_user

create_time, delete_time = [], []

kb = ["🔑Код"]

f_bot_token = open("bot_token.txt", "r", encoding='utf-8')

bot_token = f_bot_token.read()
bot = telebot.TeleBot(bot_token)

def mult_threading(func):
    @wraps(func)
    def wrapper(*args_, **kwargs_):
        func_thread = threading.Thread(target=func,
                                       args=tuple(args_),
                                       kwargs=kwargs_)
        func_thread.daemon = True
        func_thread.start()
        return func_thread

    return wrapper

@mult_threading
def create_user():
    with open("schedule.csv", 'r', encoding='utf-8') as schedule_file:
        reader = csv.DictReader(schedule_file, delimiter=',')
        lenght = len(list(reader))
        for row in reader:
            create_time.append(row["create"])
            delete_time.append(row["remove"])
        schedule_file.close()
    for i in range(0, lenght):
        schedule.every().day.at(create_time[i]).do(add_user(i))
        schedule.every().day.at(delete_time[i]).do(remove_user(i))
    while True:
        schedule.run_pending()
        time.sleep(1)

@mult_threading
def update_users():
    while True:
        global allowed_users
        global admins
        allowed_users = []
        with open("users.csv", 'r', encoding='utf-8') as users_file:
            reader = csv.DictReader(users_file, delimiter=',')
            for row in reader:
                allowed_users.append(row["id"])
            users_file.close()
        time.sleep(3)

def get_code():
    dict = rosapi.list_users.get()[1]
    return dict.get('name')

def tbot():
    def addKB(message):
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        key = types.KeyboardButton(kb[0])
        markup.row(key)
        bot.send_message(message.chat.id, "Оберіть дію:", reply_markup=markup)

    @bot.message_handler(func=lambda message: str(message.chat.id) not in allowed_users)
    def some(message):
        bot.send_message(message.chat.id, f"Ваш Telegram ідентифікатор: {message.chat.id}.\nЗверніться до системного адміністратора")

    @bot.message_handler(commands=['start'])
    def start(message):
        addKB(message)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        addKB(message)

    @bot.message_handler(func=lambda message: message.text == str(kb[0]))
    def send_code(message):
        try:
            bot.send_message(message.chat.id, get_code())
        except:
            bot.send_message(message.chat.id, "None")

    bot.infinity_polling()

def main():
    update_users()
    create_user()
    tbot()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()