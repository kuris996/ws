import sqlite3
import asyncio


class Consignee:
    columns = ['id', 'consignee', 'station', 'region', 'holding', 'GPS_latitude', 'GPS_longitude', 'year']

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM consignee")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit, sorter):
        try:
            cursor = self.__db.cursor()
            sql = "SELECT * FROM consignee "
            if sorter != None:
                sql += "ORDER BY {} ".format(sorter['field'])
                if sorter['order'] == 'descend':
                    sql += "DESC "
            sql += "LIMIT {}, {}".format(offset, limit)
            cursor.execute(sql)
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Consignee.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO consignee("
                "   consignee,"
                "   station,"
                "   region,"
                "   holding,"
                "   GPS_latitude,"
                "   GPS_longitude,"
                "   year) "
                "VALUES(?, ?, ?, ?, ?, ?, ?)",
                (record['consignee'],
                record['station'],
                record['region'],
                record['holding'],
                record['GPS_latitude'],
                record['GPS_longitude'],
                record['year'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE consignee SET"
                "   consignee = ?,"
                "   station = ?,"
                "   region = ?," 
                "   holding = ?,"
                "   GPS_latitude = ?,"
                "   GPS_longitude = ?,"
                "   year = ?"
                "WHERE id = ?",
                (record['consignee'],
                record['station'],
                record['region'],
                record['holding'],
                record['GPS_latitude'],
                record['GPS_longitude'],
                record['year'],
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
            cursor.execute("DELETE FROM consignee WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None