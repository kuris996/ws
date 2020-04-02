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
        kit = Kit(self.request.app.db, self.request.app.db_lock)
        method = record['method']
        if method == 'add':
            _record = (record['uuid'],
                       datetime.datetime.now(),
                       None,
                       None,
                      'idle')
            id = await kit.add(_record)
            #await self.run(id, record)
        return await self.get()