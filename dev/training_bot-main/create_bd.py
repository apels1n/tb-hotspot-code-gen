import sqlite3 as sql
import datetime
import os
from exercises_base import exercises_insert
from gyms_base import gyms_insert


def create_db():
    if os.path.isfile('db.db'):
        os.remove('db.db')

    with sql.connect('db.db') as db:
        # Если файл уже существует, то функция connect осуществит подключение к нему.

        # Еще один способ создания баз данных с помощью SQLite в Python — создание их в памяти.
        # Это отличный вариант для тестирования, ведь такие базы существуют только в оперативной памяти.
        #
        # conn = sqlite3.connect(:memory:)

        curs = db.cursor()

        curs.execute("PRAGMA foreign_keys = ON")
        # Сохраняем изменения
        db.commit()

        # создание таблицы exercises
        curs.execute("""CREATE TABLE IF NOT EXISTS exercises (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        muscle TEXT,
                        name TEXT)
                    """)
        # Сохраняем изменения
        db.commit()

        # создание таблицы gyms
        curs.execute("""
            CREATE TABLE IF NOT EXISTS gyms (
                name TEXT NOT NULL PRIMARY KEY,
                address TEXT)
            """)
        db.commit()

        # создание таблицы trainings
        curs.execute("""
            CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                gym_name TEXT NOT NULL REFERENCES gyms (name),
                exercise_id TEXT NOT NULL REFERENCES exercises (id),
                weight INTEGER,
                reps INTEGER )
            """)
        db.commit()

        try:
            exercises_insert()
        except:
            pass
        try:
            gyms_insert()
        except:
            pass
