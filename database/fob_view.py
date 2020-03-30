from aiohttp import web
from database.fob import Fob
from pagination import Pagination

import simplejson as json
import functools


class FobView(Pagination):
    async def fetch(self, current_page, page_size, sorter, rest):
        fob = Fob(self.request.app.db_ref)
        total = await fob.count()
        filters = await fob.fetch_filters()
        data_source = await fob.fetch((current_page - 1) * page_size, page_size, sorter, rest)
        return total, data_source, filters

    async def remove(self, id):
        fob = Fob(self.request.app.db_ref)
        await fob.remove(id)

    async def add(self, record):
        fob = Fob(self.request.app.db_ref)
        await fob.add(record)

    async def update(self, record):
        fob = Fob(self.request.app.db_ref)
        await fob.update(record)