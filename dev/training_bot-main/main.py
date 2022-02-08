import datetime

import telebot  # pip install pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import token
from create_bd import create_db
import db_functions

import re


gym = ''
exex = ''

bot = telebot.TeleBot(token)


def gen_main_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Список залов", callback_data="/gyms"),
               InlineKeyboardButton("Список упражений", callback_data="/exercises"),
               InlineKeyboardButton("Начать тренировку", callback_data="/add_training"))
    return markup


@bot.message_handler(commands=['start', 'main_menu'])
def start_message(message):
    bot.send_message(message.chat.id, "Чем займемся?", reply_markup=gen_main_markup())


def gyms_list_str():
    gyms_list = ''
    for i in db_functions.get_gyms_list():
        gyms_list += f'{i[0]}. Находится: {i[1]}\n'
    return gyms_list


def exercises_list_str():
    exercises_list = ''
    for i in db_functions.get_exercises_list():
        exercises_list += f'{i[1]} ({i[0]})\n'
    return exercises_list


# ===================== Обработчик текстовых сообщений =====================
# Здесь обрабатывается сообщение с параметрами подхода и сам подход добавляется в БД
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    global gym
    global exex
    if re.fullmatch('[0-9]+\s[0-9]+', message.text.strip()) and gym != '' and exex != '':
        db_functions.add_exercise([datetime.datetime.now(),
                                   gym,
                                   exex,
                                   message.text.strip().split(' ')[0],
                                   message.text.strip().split(' ')[1]])

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Новое упражнение', callback_data='/new_ex'),
                   InlineKeyboardButton('Добавить подход', callback_data='/new_rep'),
                   InlineKeyboardButton("Закончить тренировку", callback_data="/end_training"))
        bot.send_message(message.chat.id, 'Подход записан!', reply_markup=markup)
    elif gym != '' or exex != '':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Новое упражнение', callback_data='/new_ex'),
                   InlineKeyboardButton('Добавить подход', callback_data='/new_rep'),
                   InlineKeyboardButton("Закончить тренировку", callback_data="/end_training"))
        bot.send_message(message.chat.id,
                         'Некорректные данные. Подход НЕ записан!\n'
                            f'Зал: {gym}. Упражнение: {exex}.\n'
                            'Введите данные подхода в формате: вес кол-во',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Чем займемся?", reply_markup=gen_main_markup())


# ======================== Главное меню ==================
def get_gyms_names():
    gyms_names = []
    for i in db_functions.get_gyms_list():
        gyms_names.append(i[0])
    return gyms_names


def get_exercises_names():
    exercises_names = []
    for i in db_functions.get_exercises_list():
        exercises_names.append(i[1])
    return exercises_names


def gen_gyms_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for g in get_gyms_names():
        markup.add(InlineKeyboardButton(g, callback_data=g))
    return markup


def gen_exercises_markup():
    markup = InlineKeyboardMarkup()
    for ex in db_functions.get_exercises_list():
        markup.add(InlineKeyboardButton(f'{ex[1]} ({ex[0]})', callback_data=ex[1]))
    return markup


# Обработчик нажатия на кнопки. Именно здесь заключена основная логика бота.
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global gym
    global exex
    # Выводим список упражнений
    if call.data == "/exercises":
        bot.send_message(
            call.message.chat.id,
            f'{exercises_list_str()}/main_menu'
        )
    # Выводим спиок залов
    elif call.data == "/gyms":
        # print(call)
        bot.send_message(
            call.message.chat.id,
            f'{gyms_list_str()}/main_menu'
        )
    # Создаем меню выбора залов
    elif call.data == '/add_training':
        gym = ''
        bot.send_message(
            call.message.chat.id,
            f'Выбрать зал:',
            reply_markup=gen_gyms_markup()
        )
    # Создаем меню подтверждения добавления упражнения
    elif call.data in get_gyms_names():
        gym = call.data
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Новое упражнение', callback_data='/new_ex'),
                   InlineKeyboardButton('Выбрать другой зал', callback_data='/add_training'))
        bot.send_message(
            call.message.chat.id,
            f'Выбран зал: {gym}',
            reply_markup=markup
        )
    # Создаем меню выбора упражнения
    elif call.data == '/new_ex':
        exex = ''
        bot.send_message(
            call.message.chat.id,
            f'Выбрать упражнение:',
            reply_markup=gen_exercises_markup()
        )
    # Создаем меню подтверждения добавления подхода
    elif call.data in get_exercises_names():
        exex = call.data
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Добавить подход', callback_data='/new_rep'),
                   InlineKeyboardButton('Выбрать другое упражнение', callback_data='/new_ex'))
        bot.send_message(
            call.message.chat.id,
            f'Выбрано упражнение: {exex}',
            reply_markup=markup
        )
    # Выводим информацию по добавлению подхода
    elif call.data == '/new_rep':
        bot.send_message(
            call.message.chat.id,
            f'Зал: {gym}. Упражнение: {exex}.\nВведите данные подхода в формате: вес кол-во'
        )
    # Информируем о завершении тренировки.
    elif call.data == '/end_training':
        gym = ''
        exex = ''
        bot.send_message(call.message.chat.id, "Время отдыха?", reply_markup=gen_main_markup())


print('Bot in work....')
create_db()
bot.polling(none_stop=True, interval=0)
