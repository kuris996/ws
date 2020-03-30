import sqlite3
import datetime

class Task:
    columns = ['id', 'product', 'createdAt', 'startedAt', 'finishedAt', 'percent', 'status']

    def __init__(self, db, lock):
        self.__db = db
        self.__lock = lock

    async def count(self):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            result = cursor.fetchone()
            return result[0]
        except sqlite3.Error as error:
            return None
        finally:
            self.__lock.release()

    async def fetch(self, offset, limit, sorter):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            sql = "SELECT * FROM tasks "
            if sorter != None:
                sql += "ORDER BY {} ".format(sorter['field'])
                if sorter['order'] == 'descend':
                    sql += "DESC "
            sql += "LIMIT {}, {}".format(offset, limit)
            cursor.execute(sql)
            result = cursor.fetchall()
            rows = []
            for row in result:
                d = dict(zip(Task.columns, row)) # a dict with column names as keys
                rows.append(d)
            return rows
        except sqlite3.Error as error:
            return None
        finally:
            self.__lock.release()

    async def add(self, product):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute(
                "INSERT INTO tasks ("
                "   product,"
                "   createdAt, "
                "   startedAt, "
                "   finishedAt, "
                "   percent, "
                "   status"
                ")"
                "VALUES(?, ?, ?, ?, ?, ?)",
                (   
                    product,
                    datetime.datetime.now(),
                    None,
                    None,
                    0,
                    "idle"
                )
            )
            self.__db.commit()
            return cursor.lastrowid
        except sqlite3.Error as error:
            return None
        finally:
            self.__lock.release()

    async def remove(self, id):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            s = ','.join(str(x) for x in id)
            cursor.execute("DELETE FROM tasks WHERE id IN ({})".format(s))
            self.__db.commit()
            return id
        except:
            return None
        finally:
            self.__lock.release()

    def update_status(self, record):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute(
                "UPDATE tasks SET"
                "   startedAt = ?,"
                "   finishedAt = ?,"
                "   status = ?"
                "WHERE id = ?",
                (record['startedAt'],
                record['finishedAt'],
                record['status'],
                record['id'])
            )
            self.__db.commit()
            return True
        except:
            return None
        finally:
            self.__lock.release()
