import sqlite3
import datetime

from model import Model

class Backtesting(Model):
    def __init__(self, db, lock = None):
        super().__init__(db, lock)
        self.__db = db
        self.table_name = "backtesting"
        self.columns = ['id', 'createdAt', 'startedAt', 'finishedAt', 'status']
        self.filters = ['status']

    async def fetch_more(self, cursor, items):
        cursor.row_factory = lambda cursor, row: dict(zip(['product', 'kitName', 'kit', 'createdAt'], row))
        for item in items:
            cursor.execute(
                "SELECT product, kitName, task.kit as kit, task.createdAt as createdAt "
                "FROM task, backtesting_task "
                "WHERE {} == backtesting_task.backtestingId"
                "  AND task.id == backtesting_task.taskId".format(item['id']))
            tasks = cursor.fetchall()
            item['tasks'] = tasks
        return items

    async def add_more(self, cursor, lastrowid, items):
        sql = "INSERT INTO backtesting_task (backtestingId, taskId) VALUES(?,?)"
        for key, item in items.items():
            cursor.execute(sql, (lastrowid, int(item['id'])))

    async def remove_more(self, cursor, id):
        for x in id:
            sql = "DELETE FROM backtesting_task WHERE backtestingId = {}".format(str(x))
            cursor.execute(sql)

    def update_status(self, record):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            cursor.execute(
                "UPDATE backtesting SET"
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
            self.lock_release()