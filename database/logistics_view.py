from aiohttp import web
from database.logistics import Logistics
from pagination import Pagination

import simplejson as json
import functools


class LogisticsView(Pagination):
    async def fetch(self, current_page, page_size, sorter):
        logistics = Logistics(self.request.app.db_ref)
        total = await logistics.count()
        data_source = await logistics.fetch((current_page - 1) * page_size, page_size, sorter)
        return total, data_source

    async def remove(self, id):
        logistics = Logistics(self.request.app.db_ref)
        await logistics.remove(id)

    async def add(self, record):
        logistics = Logistics(self.request.app.db_ref)
        await logistics.add(record)

    async def update(self, record):
        logistics = Logistics(self.request.app.db_ref)
        await logistics.update(record)