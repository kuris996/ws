import sqlite3
import asyncio


class Holding:
    columns = ['id', 'factory', 'holding']

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM holding")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit, sorter):
        try:
            cursor = self.__db.cursor()
            sql = "SELECT * FROM holding "
            if sorter != None:
                sql += "ORDER BY {} ".format(sorter['field'])
                if sorter['order'] == 'descend':
                    sql += "DESC "
            sql += "LIMIT {}, {}".format(offset, limit)
            cursor.execute(sql)
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Holding.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO holding("
                "   factory,"
                "   holding) "
                "VALUES(?, ?)",
                (record['factory'],
                record['holding'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE holding SET"
                "   factory = ?,"
                "   holding = ?"
                "WHERE id = ?",
                (record['factory'],
                record['holding'],
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
            cursor.execute("DELETE FROM holding WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None