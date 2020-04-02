import sqlite3
import datetime

from model import Model

class Kit(Model):
    def __init__(self, db, lock = None):
        super().__init__(db, lock)
        self.__db = db
        self.table_name = "kit"
        self.columns = ['id', 'uuid', 'createdAt', 'startedAt', 'finishedAt', 'status']
        self.filters = ['status']
    