import sqlite3
import datetime
import re


class Task:
    columns = ['id', 'product', 'createdAt', 'startedAt', 'finishedAt', 'percent', 'status']

    def __init__(self, db, lock):
        self.__db = db
        self.__lock = lock

    async def fetch(self):
        try:
            self.__lock.acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT * FROM tasks")
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