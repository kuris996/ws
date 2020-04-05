import sqlite3
import datetime

from model import Model

class Kit(Model):
    def __init__(self, db, lock = None):
        super().__init__(db, lock)
        self.__db = db
        self.table_name = "kit"
        self.columns = ['id', 'uuid', 'name', 'createdAt', 'startedAt', 'finishedAt', 'status']
        self.filters = ['status']
    
    def update_status(self, record):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            cursor.execute(
                "UPDATE kit SET"
                "   startedAt = ?,"
                "   finishedAt = ?,"
                "   status = ?"
                "WHERE uuid = ?",
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