# -*- coding: utf-8 -*-
import csv
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
    with open("schedule.csv", 'r') as schedule_file:
        reader = csv.DictReader(schedule_file, delimiter=',')
        for row in reader:
            create_time.append(row["create"])
            delete_time.append(row["remove"])
        schedule_file.close()
    schedule.every().day.at(create_time[0]).do(add_user)
    schedule.every().day.at(delete_time[0]).do(remove_user)
    schedule.every().day.at(create_time[1]).do(add_user)
    schedule.every().day.at(delete_time[1]).do(remove_user)
    schedule.every().day.at(create_time[2]).do(add_user)
    schedule.every().day.at(delete_time[2]).do(remove_user)
    schedule.every().day.at(create_time[3]).do(add_user)
    schedule.every().day.at(delete_time[3]).do(remove_user)
    schedule.every().day.at(create_time[4]).do(add_user)
    schedule.every().day.at(delete_time[4]).do(remove_user)
    schedule.every().day.at(create_time[5]).do(add_user)
    schedule.every().day.at(delete_time[5]).do(remove_user)
    schedule.every().day.at(create_time[6]).do(add_user)
    schedule.every().day.at(delete_time[6]).do(remove_user)
    schedule.every().day.at(create_time[7]).do(add_user)
    schedule.every().day.at(delete_time[7]).do(remove_user)
    while True:
        schedule.run_pending()
        time.sleep(1)

@mult_threading
def update_users():
    while True:
        global allowed_users
        global admins
        allowed_users = []
        with open("users.csv", 'r') as users_file:
            reader = csv.DictReader(users_file, delimiter=',')
            for row in reader:
                allowed_users.append(row["id"])
            users_file.close()
        time.sleep(3)

def tbot():
    def addKB(message):
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        key = types.KeyboardButton(kb[0])
        markup.row(key)
        bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

    @bot.message_handler(func=lambda message: str(message.chat.id) not in allowed_users)
    def some(message):
        return False

    @bot.message_handler(commands=['start'])
    def start(message):
        addKB(message)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        addKB(message)

    @bot.message_handler(func=lambda message: message.text == str(kb[0]))
    def send_code(message):
        try:
            bot.send_message(message.chat.id, rosapi.name)
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