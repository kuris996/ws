from aiohttp import web
from calculation.backtesting import Backtesting
from pagination import Pagination
from collections import defaultdict

import simplejson as json
import functools
import requests
import datetime

class BacktestingView(Pagination):
    async def fetch(self, current_page, page_size, sorter, rest):
        backtesting = Backtesting(self.request.app.db, self.request.app.db_lock)
        total = await backtesting.count()
        filters = await backtesting.fetch_filters()
        data_source = await backtesting.fetch((current_page - 1) * page_size, page_size, sorter, rest)
        return total, data_source, filters

    async def remove(self, id):
        backtesting = Backtesting(self.request.app.db, self.request.app.db_lock)
        await backtesting.remove(id)

    async def add(self, record):
        backtesting = Backtesting(self.request.app.db, self.request.app.db_lock)
        backtesting_kits = defaultdict(dict)
        for key, value in record.items():
            kit = value['kit']
            backtesting_kits[kit][key] = value
        for key, value in backtesting_kits.items():
            _record = (datetime.datetime.now(), None, None, 'idle')
            id = await backtesting.add(_record, value)
            await self.run(id, key, value)

    async def run(self, id, kit, record):
        config_id = []
        for key, value in record.items():
            config_id.append(value['uuid'])
        body = {
            "ID": id,
            "Config" : {
                "data_id" : str(kit),
                "config_id" : config_id,
                "fact_file" : "act_v5.xlsx"
            }
        }
        try:
            headers = {'Content-type': 'application/json'}
            requests.post(self.request.app.engine_endpoint + "/backtesting", 
                json=body,
                headers=headers)
        except Exception as e:
            print('[ws]: could not request', str(e))


