import sqlite3
import asyncio


class PerevalkaUpakovka:
    columns = ['id', 'year', 'month', 'perevalka_rub', 'perevalka_dollar', 'upakovka_rub', 'upakovka_dollar']

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM perevalka_upakovka")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT * FROM perevalka_upakovka LIMIT {}, {}".format(offset, limit))
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(PerevalkaUpakovka.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO perevalka_upakovka("
                "   year,"
                "   month,"
                "   perevalka_rub,"
                "   perevalka_dollar," 
                "   upakovka_rub,"
                "   upakovka_dollar) "
                "VALUES(?, ?, ?, ?, ?, ?)",
                (record['year'],
                record['month'],
                record['perevalka_rub'],
                record['perevalka_dollar'],
                record['upakovka_rub'],
                record['upakovka_dollar'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE perevalka_upakovka SET"
                "   year = ?,"
                "   month = ?,"
                "   perevalka_rub = ?," 
                "   perevalka_dollar = ?,"
                "   upakovka_rub = ?,"
                "   upakovka_dollar = ?"
                "WHERE id = ?",
                (record['year'],
                record['month'],
                record['perevalka_rub'],
                record['perevalka_dollar'],
                record['upakovka_rub'],
                record['upakovka_dollar'],
                record['id'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def remove(self, id):
        cursor = self.__db.cursor()
        try:
            s = ','.join(str(x) for x in id)
            cursor.execute("DELETE FROM perevalka_upakovka WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None