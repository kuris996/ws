import sqlite3

class Model:
    def __init__(self, db, lock):
        self.__db = db
        self.__lock = lock

    def __lock_acquire(self):
        if self.__lock == None:
            return
        self.__lock.acquire()

    def __lock_release(self):
        if self.__lock == None:
            return
        self.__lock.release()

    def count(self):
        try:
            self.__lock_acquire()
            cursor = self.__db.cursor()
            cursor.execute("SELECT COUNT(*) FROM {}".format(self.table_name))
            result = cursor.fetchone()
            return result[0]
        except:
            return None
        finally:
            self.__lock_release()

    def fetch_filters(self):
        try: 
            self.__lock_acquire()
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
            self.__lock_release()

    def fetch(self, offset, limit, sorter, filters):
        try:
            self.__lock_acquire()
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
            return cursor.fetchall()
        except:
            return None
        finally:
            self.__lock_release()

    def add(self, record):
        try:
            self.__lock_acquire()
            cursor = self.__db.cursor()
            sql = "INSERT INTO {} ({}) VALUES({})".format(
                self.table_name, 
                ", ".join(self.columns[1:]), 
                ", ".join("?" for i in range(len(self.columns[1:]))))
            cursor.execute(sql, (*record.values(),))
            self.__db.commit()
            return cursor.lastrowid
        except:
            return None
        finally:
            self.__lock_release()

    def update(self, record):
        try:
            self.__lock_acquire()
            cursor = self.__db.cursor()
            sql = "UPDATE {} SET {} = ? WHERE id = ?".format(
                self.table_name,
                " = ?, ".join(self.columns[1:])
            )
            cursor.execute(sql, (*record.values(), record['id'])[1:])
            self.__db.commit()
            return True
        except:
            return None
        finally:
            self.__lock_release()

    def remove(self, id):
        try:
            self.__lock_acquire()
            cursor = self.__db.cursor()
            cursor.execute("DELETE FROM {} WHERE id IN ({})".format(
                self.table_name, ','.join(str(x) for x in id))
            )
            self.__db.commit()
            return True
        except:
            return None
        finally:
            self.__lock_release()