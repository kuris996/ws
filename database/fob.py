import sqlite3
import asyncio

from model import Model


class Fob(Model):
    columns = ['id', 'product', 'year', 'month', 'seller', 'foreign_price', 'foreign_costs']
    filters = ['product', 'year', 'month', 'seller']

    def __init__(self, db, lock = None):
        super().__init__(db, lock)
        self.__db = db
        self.table_name = "FOB"
        self.columns = ['id', 'product', 'year', 'month', 'seller', 'foreign_price', 'foreign_costs']
        self.filters = ['product', 'year', 'month', 'seller']

    