import sqlite3 as sql


def exercises_insert():
    with sql.connect('db.db') as db:
        curs = db.cursor()

        chest = [
            'Жим лежа',
            'Жим на наклонной скамье',
            'Разводка на наклонной скамье',
            'Кроссовер',
            'Сведение рук в тренажере',
            'Отжимания на брусьях',

        ]

        for i in chest:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['chest', i])
            db.commit()

        back = [
            'Тяга вниз широким хватом',
            'Тяга штанги в наклоне',
            'Тяга гантели в наклоне',
            'Горизонтальная тяга',
            'Гиперэкстензия',
            'Подтягивания',
        ]

        for i in back:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['back', i])
            db.commit()

        legs = [
            'Присед со штангой',
            'Бицепс ног',
            'Трицепс ног',
        ]

        for i in legs:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['legs', i])
            db.commit()

        biceps = [
            'Подъем гантелей сидя'
        ]

        for i in biceps:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['biceps', i])
            db.commit()

        triceps = [
            'Тяга в тренажере'
        ]

        for i in triceps:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['triceps', i])
            db.commit()

        abc = [
            'Прямые скручивания'
        ]

        for i in abc:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['abc', i])
            db.commit()

        shoulders = [
            'Жим гантелей от плеч',
            'Подъем гантелей в стороны',
            'Подъем гантелей вперед',
            'Подъем гантелей в наклоне',
        ]

        for i in shoulders:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['shoulders', i])
            db.commit()

        warmup = [
            'Бег',
            'Отжимания на брусьях',
            'Подтягивания',
            'Элептический тренажер',
            'Велотренажер',
        ]

        for i in warmup:
            curs.execute("""INSERT INTO exercises (muscle, name) 
                        values (?,?)""",
                        ['warmup', i])
            db.commit()
