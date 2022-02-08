import sqlite3 as sql


def gyms_insert():
    gyms_list = [
        ['Щорса', 'На Щорса'],
        ['Лента', 'На Богданке'],
        ['Гринн', 'В Гринне']
    ]
    with sql.connect('db.db') as db:
        curs = db.cursor()

        zapros = """insert into gyms (name, address)
                    values (?,?);"""
        curs.executemany(zapros,
                    gyms_list)
        db.commit()

