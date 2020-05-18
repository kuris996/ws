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
        id = None
        try:
            task = Task(self.request.app.db, self.request.app.db_lock)
            _record = (record['uuid'], record['kit'], record['PRODUCT'], record['kitName'], datetime.datetime.now(), None, None, 'idle')
            id = await task.add(_record)
            await self.run(id, record)
        except:
            _record = (record['uuid'], record['kit'], record['PRODUCT'], record['kitName'], datetime.datetime.now(), None, None, 'idle', id)
            await task.update(_record)

    async def run(self, id, record):
        _type = record['CALCULATION_TYPE_ID']
        body = {}
        if _type == 1:
            body = {
                "ID": str(id),
                "Config": {
                    "DATA_ID": str(record['kit']),
                    "CONFIG_ID": str(record['uuid']),
                    "CALCULATION_TYPE_ID" : _type - 1,
                    "DELTA": [float(record['DELTA'])],
                    "START_PRICE": float(record['START_PRICE']),
                    "REARRANGE_HOLDINGS": bool(record['REARRANGE_HOLDINGS'])
                }
            }
        elif _type == 2:
            body = {
                "ID": str(id),
                "Config": {
                    "DATA_ID": str(record['kit']),
                    "CONFIG_ID": str(record['uuid']),
                    "PRODUCT": str(record['PRODUCT']),
                    "CALCULATION_TYPE_ID" : _type - 1,
                    "DELTAS_STORAGE": [float(record['DELTAS_STORAGE'])],
                    "DELTA_RAILWAY": [float(record['DELTA_RAILWAY'])],
                    "YEARS": record['YEARS'],
                    "RAILWAY_INITIAL_PRICE": int(record['RAILWAY_INITIAL_PRICE']),
                    "MAX_RATIO_RAILWAY": int(record['MAX_RATIO_RAILWAY']),
                    "STORAGES_BUY_ON_MARKET": bool(record['STORAGES_BUY_ON_MARKET']),                    
                    "AUTO_OPEN_STORAGE": bool(record['AUTO_OPEN_STORAGE']),                    
                    "ALTERNATIVE_PREMIUM": int(record['ALTERNATIVE_PREMIUM']),
                    "LOGISTIC_PREMIUM": int(record['LOGISTIC_PREMIUM']),
                    "MIN_RADIUS": int(record['MIN_RADIUS']),
                    "MAX_RADIUS": int(record['MAX_RADIUS']),
                    "CUSTOMER_DISTANCE": float(record['CUSTOMER_DISTANCE']),
                    "AVAILABILITY_RADIUS": int(record['AVAILABILITY_RADIUS']),
                    "STORAGE_PRICE": int(record['STORAGE_PRICE']),
                    "BALANCE_RATIO": float(record['BALANCE_RATIO']),
                    "REARRANGE_HOLDINGS": bool(record['REARRANGE_HOLDINGS']),
                    "SHUFFLE_STORAGE": bool(record['SHUFFLE_STORAGE']),
                    "SHUFFLE_RAILWAY": bool(record['SHUFFLE_RAILWAY']),
                    "CORRECTION_FLAG": bool(record['CORRECTION_FLAG']),
                    "CORRECTION_CORIDOR": list(map(float, record['CORRECTION_CORIDOR'].split(',')))
                }
            }
        headers = {'Content-type': 'application/json'}
        requests.post(self.request.app.engine_endpoint + "/run", 
            json=body,
            headers=headers)
