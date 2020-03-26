from aiohttp import web
from database.holding import Holding
from pagination import Pagination

import simplejson as json
import functools


class HoldingView(Pagination):
    async def fetch(self, current_page, page_size):
        holding = Holding(self.request.app.db_ref)
        total = await holding.count()
        data_source = await holding.fetch((current_page - 1) * page_size, page_size)
        return total, data_source

    async def remove(self, id):
        holding = Holding(self.request.app.db_ref)
        await holding.remove(id)

    async def add(self, record):
        holding = Holding(self.request.app.db_ref)
        await holding.add(record)

    async def update(self, record):
        holding = Holding(self.request.app.db_ref)
        await holding.update(record)