from aiohttp import web
from database.factory import Factory
from pagination import Pagination

import simplejson as json
import functools


class FactoryView(Pagination):
    async def fetch(self, current_page, page_size):
        factory = Factory(self.request.app.db_ref)
        total = await factory.count()
        data_source = await factory.fetch((current_page - 1) * page_size, page_size)
        return total, data_source

    async def remove(self, id):
        factory = Factory(self.request.app.db_ref)
        await factory.remove(id)

    async def add(self, record):
        factory = Factory(self.request.app.db_ref)
        await factory.add(record)

    async def update(self, record):
        factory = Factory(self.request.app.db_ref)
        await factory.update(record)