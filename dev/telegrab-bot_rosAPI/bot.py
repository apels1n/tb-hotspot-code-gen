# -*- coding: utf-8 -*-
import time
import rosapi
import telebot
import schedule
import threading
from telebot import types
from functools import wraps
from rosapi import add_user

bot_token = '5176295217:AAEJBHJZch0iA49SL4eorapkFyqFB6pPGtk'
bot = telebot.TeleBot(bot_token)

kb = ["🔑Код"]

f_users = open("users.txt", "r", encoding='utf-8')
#f_users = 342412557

def mult_threading(func):
    """Декоратор для запуска функции в отдельном потоке"""

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
    schedule.every(10).seconds.do(add_user)
    schedule.run_pending()
    while True:
        schedule.run_pending()
        time.sleep(1)

def tbot():
    def addKB(message):
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
        key = types.KeyboardButton(kb[0])
        markup.row(key)
        bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def start(message):
        addKB(message)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        addKB(message)

    @bot.message_handler(commands=['auto_nf'])
    def auto_nf(message):
        bot.send_message(message.chat.id, "rosapi.name")

    @bot.message_handler(func=lambda message: message.text == str(kb[0]))
    def send_code(message):
        try:
            bot.send_message(message.chat.id, rosapi.name)
        except:
            bot.send_message(message.chat.id, "None")

    bot.infinity_polling()

def main():
    create_user()
    tbot()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()