import sqlite3 as sql

def main():
    with sql.connect('db.db') as db:
        curs = db.cursor()
        curs.execute("""Select id from users""")
        print(curs.fetchall())
        if curs.fetchall() == 1548745:
            print("hui")


if __name__ == '__main__':
    main()