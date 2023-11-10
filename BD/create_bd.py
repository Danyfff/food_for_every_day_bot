import sqlite3 as sq

db = sq.connect('BD/recrpts.db')
cur = db.cursor()


def db_start(name_tadle):
    cur.execute(f"CREATE TABLE IF NOT EXISTS {name_tadle}("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name_subcate TEXT,"
                "name_recept TEXT,"
                "href_recept TEXT)")


def add_recept(name_table, recept_data):
    cur.execute(f"INSERT INTO {name_table} (name_subcate, name_recept, href_recept) VALUES ('{recept_data[0]}', '{recept_data[1]}', '{recept_data[2]}')")
                # (recept_data[1]['name_subcate'], recept_data[2]['name_recept'], recept_data[3]['href_recept']))
    db.commit()


def db_close():
    cur.close()
