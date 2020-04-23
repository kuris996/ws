from aiohttp import web
from calculation.kit import Kit
from pagination import Pagination

import simplejson as json
import functools
import requests
import datetime

class KitView(Pagination):
    async def fetch(self, current_page, page_size, sorter, rest):
        kit = Kit(self.request.app.db, self.request.app.db_lock)
        total = await kit.count()
        filters = await kit.fetch_filters()
        data_source = await kit.fetch((current_page - 1) * page_size, page_size, sorter, rest)
        return total, data_source, filters

    async def remove(self, id):
        kit = Kit(self.request.app.db, self.request.app.db_lock)
        await kit.remove(id)

    async def add(self, record):
        id = None
        try:
            kit = Kit(self.request.app.db, self.request.app.db_lock)
            _record = (record['uuid'], record['name'], datetime.datetime.now(), None, None, 'idle')
            id = await kit.add(_record)
            if record['type'] == 1:
                await self.run(record)
        except:
            _record = (record['uuid'], record['name'], datetime.datetime.now(), None, None, 'error', id)
            await kit.update(_record)

    async def run(self, record):
        body = { "ID": str(record['uuid']) }
        headers = {'Content-type': 'application/json'}
        requests.post(self.request.app.engine_endpoint + "/update_inputs", 
            json = body,
            headers=headers)
