import sqlite3
import asyncio


class Factory:
    columns = ['id', 'product', 'seller', 'factory']

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM factory")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT * FROM factory LIMIT {}, {}".format(offset, limit))
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Factory.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO factory("
                "   product,"
                "   seller,"
                "   factory) "
                "VALUES(?, ?, ?)",
                (record['product'],
                record['seller'],
                record['factory'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE factory SET"
                "   product = ?,"
                "   seller = ?,"
                "   factory = ?"
                "WHERE id = ?",
                (record['product'],
                record['seller'],
                record['factory'],
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
            cursor.execute("DELETE FROM factory WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None