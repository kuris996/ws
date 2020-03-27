import sqlite3
import datetime
import re
import requests

ENGINE_ENDPOINT = "http://127.0.0.1:8090/run"

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

    async def request(self, id, request):
        body = {
            "ID" : id,
            "Config": {
                "PRODUCT": request['PRODUCT'],
                "DELTAS_STORAGE": list(map(float, request['DELTAS_STORAGE'].split(','))),
                "DELTA_RAILWAY": list(map(float, request['DELTA_RAILWAY'].split(','))),
                "FILENAMES_DICT": {
                    "январь": "январь.xlsx",
                    "февраль": "февраль.xlsx",
                    "март": "март.xlsx",
                    "апрель": "апрель.xlsx",
                    "may": "may.xlsx",
                    "июнь": "июнь.xlsx",
                    "июль": "июль.xlsx",
                    "август": "август.xlsx",
                    "сентябрь": "сентябрь.xlsx",
                    "октябрь": "октябрь.xlsx",
                    "ноябрь": "ноябрь.xlsx",
                    "декабрь": "декабрь.xlsx"
                },
                "YEARS": list(map(float, request['YEARS'].split(','))),
                "FOB_PRICES": list(map(float, request['FOB_PRICES'].split(','))),
                "RAILWAY_INITIAL_PRICE": request['RAILWAY_INITIAL_PRICE'],
                "MAX_RATIO_RAILWAY": request['MAX_RATIO_RAILWAY'],
                "STORAGES_BUY_ON_MARKET": request['STORAGES_BUY_ON_MARKET'],
                "CONSUMPTION_PATTERN": [
                    [
                        25.24773087,
                        21.81148346,
                        21.74587548,
                        12.79410911,
                        7.402354631,
                        5.965056163,
                        7.026424102,
                        8.240022611,
                        16.14207913,
                        21.73047102,
                        26.62827235,
                        30.28610832
                    ],
                    [
                        32070678.73,
                        25677220.71,
                        21249130.84,
                        22927975.89,
                        9113905.896,
                        8134107.008,
                        12537130.02,
                        24265661.91,
                        14705188.63,
                        26347669.06,
                        32206958.47,
                        31626341.32
                    ],
                    [
                        329100.6823,
                        259851.0491,
                        273844.9749,
                        135603.7924,
                        99518.38612,
                        142014.0579,
                        187259.5587,
                        254777.8027,
                        246544.2803,
                        251806.4402,
                        290891.3522,
                        373749.0662
                    ],
                    [
                        393853.2262,
                        240735.6714,
                        234335.2885,
                        169880.4367,
                        122974.1781,
                        123668.6429,
                        229471.8594,
                        214847.9185,
                        228543.4902,
                        231050.2503,
                        251663.4036,
                        276739.0158
                    ],
                    [
                        331383.5066,
                        298839.3839,
                        337555.9883,
                        260932.4071,
                        153753.8234,
                        143282.7345,
                        176481.2316,
                        120363.307,
                        105329.0482,
                        377402.1143,
                        321626.1062,
                        420731.3067
                    ]
                ],
                "PATH": {
                    "wh_prefix": "data/no_perevalka_updated_constr/railway/",
                    "wh_file": "data/no_perevalka_updated_constr/storage/Склады_",
                    "wh_add_name": "constrained"
                },
                "WH_PREMIUM_RAILWAY": request['WH_PREMIUM_RAILWAY'],
                "OVERALL_PREMIA_ADDITION": request['OVERALL_PREMIA_ADDITION'],
                "MIN_RADIUS": request['MIN_RADIUS'],
                "MAX_RADIUS": request['MAX_RADIUS'],
                "CUSTOMER_DISTANCE": request['CUSTOMER_DISTANCE'],
                "AVAILABILITY_RADIUS": request['AVAILABILITY_RADIUS'],
                "STORAGE_PRICE": request['STORAGE_PRICE'],
                "BALANCE_RATIO": request['BALANCE_RATIO'],
                "DISTANCE_PRICE": [
                    {"value": 390, "low": 0, "high": 33.33},
                    {"value": 507, "low": 33.33, "high": 66.67},
                    {"value": 581, "low": 66.67, "high": 100},
                    {"value": 752, "low": 100, "high": 133.33},
                    {"value": 926, "low": 133.33, "high": 166.67},
                    {"value": 1094, "low": 166.67, "high": 200},
                    {"value": 1241, "low": 200, "high": 233.33},
                    {"value": 1377, "low": 233.33, "high": 266.67},
                    {"value": 1e20, "low": 266.67, "high": 1e20}
                ],
                "REARRANGE_HOLDINGS": request['REARRANGE_HOLDINGS'],
                "SHUFFLE_STORAGE": request['SHUFFLE_STORAGE'],
                "SHUFFLE_RAILWAY": request['SHUFFLE_RAILWAY'],
                "CORRECTION_FLAG": request['CORRECTION_FLAG'],
                "CORRECTION_CORIDOR": list(map(float, request['CORRECTION_CORIDOR'].split(',')))
            }
        }
        req = requests.post(ENGINE_ENDPOINT, json=body)