from aiohttp import web
from database.consignee import Consignee
from pagination import Pagination

import simplejson as json
import functools


class ConsigneeView(Pagination):
    async def fetch(self, current_page, page_size):
        consignee = Consignee(self.request.app.db_ref)
        total = await consignee.count()
        data_source = await consignee.fetch((current_page - 1) * page_size, page_size)
        return total, data_source

    async def remove(self, id):
        consignee = Consignee(self.request.app.db_ref)
        await consignee.remove(id)

    async def add(self, record):
        consignee = Consignee(self.request.app.db_ref)
        await consignee.add(record)

    async def update(self, record):
        consignee = Consignee(self.request.app.db_ref)
        await consignee.update(record)