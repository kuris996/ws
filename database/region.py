import sqlite3
import asyncio


class Region:
    columns = ['id', 'station', 'region']

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM region")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit, sorter):
        try:
            cursor = self.__db.cursor()
            sql = "SELECT * FROM region "
            if sorter != None:
                sql += "ORDER BY {} ".format(sorter['field'])
                if sorter['order'] == 'descend':
                    sql += "DESC "
            sql += "LIMIT {}, {}".format(offset, limit)
            cursor.execute(sql)
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Region.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO region("
                "   station,"
                "   region) "
                "VALUES(?, ?)",
                (record['station'],
                record['region'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE region SET"
                "   station = ?,"
                "   region = ? "
                "WHERE id = ?",
                (record['station'],
                record['region'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def remove(self, id):
        cursor = self.__db.cursor()
        try:
            s = ','.join(str(x) for x in id)
            cursor.execute("DELETE FROM region WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None