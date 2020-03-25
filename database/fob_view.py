from aiohttp import web
from database.fob import Fob
from pagination import Pagination

import simplejson as json
import functools


class FobView(Pagination):
    async def fetch(self, current_page, page_size):
        fob = Fob(self.request.app.db)
        total = await fob.count()
        data_source = await fob.fetch((current_page - 1) * page_size, page_size)
        return total, data_source

    async def remove(self, id):
        fob = Fob(self.request.app.db)
        await fob.remove(id)

    async def add(self, record):
        fob = Fob(self.request.app.db)
        await fob.add(record)

    async def update(self, record):
        fob = Fob(self.request.app.db)
        await fob.update(record)