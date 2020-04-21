from aiohttp import web
from calculation.task import Task
from pagination import Pagination

import simplejson as json
import functools
import requests
import datetime

class TaskView(Pagination):
    async def fetch(self, current_page, page_size, sorter, rest):
        task = Task(self.request.app.db, self.request.app.db_lock)
        total = await task.count()
        filters = await task.fetch_filters()
        data_source = await task.fetch((current_page - 1) * page_size, page_size, sorter, rest)
        return total, data_source, filters

    async def remove(self, id):
        task = Task(self.request.app.db, self.request.app.db_lock)
        await task.remove(id)

    async def add(self, record):
        task = Task(self.request.app.db, self.request.app.db_lock)
        _record = (record['uuid'], record['kit'], record['PRODUCT'], record['kitName'], datetime.datetime.now(), None, None, 'idle')
        id = await task.add(_record)
        await self.run(id, record)

    async def run(self, id, record):
        body = {
            "ID": id,
            "Config": {
                "DATA_ID": str(record['kit']),
                "CONFIG_ID": str(record['uuid']),
                "PRODUCT": str(record['PRODUCT']),
                "DELTAS_STORAGE": list(map(float, record['DELTAS_STORAGE'].split(','))),
                "DELTA_RAILWAY": list(map(float, record['DELTA_RAILWAY'].split(','))),
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
                "YEARS": list(map(int, record['YEARS'].split(','))),
                "FOB_PRICES": list(map(int, record['FOB_PRICES'].split(','))),
                "RAILWAY_INITIAL_PRICE": int(record['RAILWAY_INITIAL_PRICE']),
                "MAX_RATIO_RAILWAY": int(record['MAX_RATIO_RAILWAY']),
                "STORAGES_BUY_ON_MARKET": bool(record['STORAGES_BUY_ON_MARKET']),
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
                    "wh_add_name": "_[P]{}_[CF]{}_[DS]{}_[SBoM]{}"
                },
                "WH_PREMIUM_RAILWAY": int(record['WH_PREMIUM_RAILWAY']),
                "OVERALL_PREMIA_ADDITION": int(record['OVERALL_PREMIA_ADDITION']),
                "MIN_RADIUS": int(record['MIN_RADIUS']),
                "MAX_RADIUS": int(record['MAX_RADIUS']),
                "CUSTOMER_DISTANCE": float(record['CUSTOMER_DISTANCE']),
                "AVAILABILITY_RADIUS": int(record['AVAILABILITY_RADIUS']),
                "STORAGE_PRICE": int(record['STORAGE_PRICE']),
                "BALANCE_RATIO": float(record['BALANCE_RATIO']),
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
                "REARRANGE_HOLDINGS": bool(record['REARRANGE_HOLDINGS']),
                "SHUFFLE_STORAGE": bool(record['SHUFFLE_STORAGE']),
                "SHUFFLE_RAILWAY": bool(record['SHUFFLE_RAILWAY']),
                "CORRECTION_FLAG": bool(record['CORRECTION_FLAG']),
                "CORRECTION_CORIDOR": list(map(float, record['CORRECTION_CORIDOR'].split(',')))
            }
        }
        try:
            headers = {'Content-type': 'application/json'}
            requests.post(self.request.app.engine_endpoint + "/run", 
                json=body,
                headers=headers)
        except Exception as e:
            print('[ws]: could not request', str(e))
