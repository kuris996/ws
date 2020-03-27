import sqlite3
import datetime
import re


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

    async def fetch(self, offset, limit):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM tasks LIMIT {}, {}".format(offset, limit))
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

    
    def fetch_running(self):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM tasks WHERE status = 'running'")
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


    def fetch_idle(self):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM tasks WHERE status = 'idle'")
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