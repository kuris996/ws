import sqlite3
import asyncio


class Logistics:
    columns = ['id', 'product', 'year', 'month', 'seller', 'buyer', 'tarif_zd_indexed', 'tarif_auto_indexex', 'logistics', 'logistics_no_perevalka' ]

    def __init__(self, db):
        self.__db = db

    async def count(self):
        cursor = self.__db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM logistics")
            result = cursor.fetchone()
            return result[0]
        except:
            return None

    async def fetch(self, offset, limit, sorter):
        try:
            cursor = self.__db.cursor()
            sql = "SELECT * FROM logistics "
            if sorter != None:
                sql += "ORDER BY {} ".format(sorter['field'])
                if sorter['order'] == 'descend':
                    sql += "DESC "
            sql += "LIMIT {}, {}".format(offset, limit)
            cursor.execute(sql)
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Logistics.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except:
            return None

    async def add(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "INSERT INTO logistics("
                "   product,"
                "   year,"
                "   month,"
                "   seller," 
                "   buyer,"
                "   tarif_zd_indexed,"
                "   tarif_auto_indexex,"
                "   logistics,"
                "   logistics_no_perevalka) "
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (record['product'],
                record['year'],
                record['month'],
                record['seller'],
                record['buyer'],
                record['tarif_zd_indexed'],
                record['tarif_auto_indexex'],
                record['logistics'],
                record['logistics_no_perevalka'])
            )
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None

    async def update(self, record):
        cursor = self.__db.cursor()
        try:
            cursor.execute(
                "UPDATE logistics SET"
                "   product = ?,"
                "   year = ?,"
                "   month = ?," 
                "   seller = ?,"
                "   buyer = ?,"
                "   tarif_zd_indexed = ?,"
                "   tarif_auto_indexex = ?,"
                "   logistics = ?,"
                "   logistics_no_perevalka = ?"
                "WHERE id = ?",
                (record['product'],
                record['year'],
                record['month'],
                record['seller'],
                record['buyer'],
                record['tarif_zd_indexed'],
                record['tarif_auto_indexex'],
                record['logistics'],
                record['logistics_no_perevalka'],
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
            cursor.execute("DELETE FROM logistics WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None