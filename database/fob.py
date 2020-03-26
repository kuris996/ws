import sqlite3
import asyncio


class Fob:
    columns = ['id', 'product', 'year', 'month', 'seller', 'foreign_price', 'foreign_costs']

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM FOB")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT * FROM FOB LIMIT {}, {}".format(offset, limit))
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Fob.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO FOB("
                "   product,"
                "   year,"
                "   month,"
                "   seller," 
                "   foreign_price,"
                "   foreign_costs) "
                "VALUES(?, ?, ?, ?, ?, ?)",
                (record['product'],
                record['year'],
                record['month'],
                record['seller'],
                record['foreign_price'],
                record['foreign_costs'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE FOB SET"
                "   product = ?,"
                "   year = ?,"
                "   month = ?," 
                "   seller = ?,"
                "   foreign_price = ?,"
                "   foreign_costs = ?"
                "WHERE id = ?",
                (record['product'],
                record['year'],
                record['month'],
                record['seller'],
                record['foreign_price'],
                record['foreign_costs'],
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
            cursor.execute("DELETE FROM FOB WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None