import sqlite3

class Model:
    def __init__(self, db, lock):
        self.__db = db
        self.__lock = lock

    def lock_acquire(self):
        if self.__lock == None:
            return
        self.__lock.acquire()

    def lock_release(self):
        if self.__lock == None:
            return
        self.__lock.release()

    async def count(self):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT COUNT(*) FROM {}".format(self.table_name))
            result = cursor.fetchone()
            return result[0]
        except:
            return None
        finally:
            self.lock_release()

    async def fetch_filters(self):
        try: 
            self.lock_acquire()
            cursor = self.__db.cursor()
            cursor.row_factory = lambda cursor, row: { "text" : row[0], "value" : row[0] }
            result = {}
            for filter in self.filters:
                sql = "SELECT DISTINCT {} FROM {} ORDER BY {}".format(filter, self.table_name, filter)
                cursor.execute(sql)
                result[filter] = cursor.fetchall()
            return result
        except:
            return None
        finally:
            self.lock_release()

    async def fetch_more(self, cursor, items):
        return items

    async def fetch(self, offset, limit, sorter, filters):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            cursor.row_factory = lambda cursor, row: dict(zip(self.columns, row))
            sql = "SELECT * FROM {} ".format(self.table_name)
            if filters != None:
                op = ""
                for key, val in filters.items():
                    if key not in self.filters:
                        continue
                    if op: 
                        sql += op
                    else:
                        sql += "WHERE"
                    sql += " {} IN ({})".format(key, val)
                    op = " AND"
            if sorter != None:
                sql += "ORDER BY {} ".format(sorter['field'])
                if sorter['order'] == 'descend':
                    sql += "DESC "
            sql += " LIMIT {}, {}".format(offset, limit)
            cursor.execute(sql)
            items = cursor.fetchall()
            return await self.fetch_more(cursor, items)
        except:
            return None
        finally:
            self.lock_release()

    async def add_more(self, cursor, lastrowid, items):
        pass

    async def add(self, record, items = None):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            sql = "INSERT INTO {} ({}) VALUES({})".format(
                self.table_name, 
                ", ".join(self.columns[1:]), 
                ", ".join("?" for i in range(len(self.columns[1:]))))
            cursor.execute(sql, record)
            lastrowid = cursor.lastrowid
            await self.add_more(cursor, lastrowid, items)
            self.__db.commit()
            return lastrowid
        except Exception as e:
            print(e)
            return None
        finally:
            self.lock_release()

    async def update(self, record, id):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            sql = "UPDATE {} SET {} = ? WHERE id = ?".format(
                self.table_name,
                " = ?, ".join(self.columns[1:])
            )
            cursor.execute(sql, record, id)
            self.__db.commit()
            return True
        except:
            return None
        finally:
            self.lock_release()

    async def remove_more(self, cursor, id):
        pass

    async def remove(self, id):
        try:
            self.lock_acquire()
            cursor = self.__db.cursor()
            cursor.execute("DELETE FROM {} WHERE id IN ({})".format(
                self.table_name, ','.join(str(x) for x in id))
            )
            await self.remove_more(cursor, id)
            self.__db.commit()
            return True
        except:
            return None
        finally:
            self.lock_release()