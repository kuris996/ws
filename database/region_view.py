from aiohttp import web
from database.region import Region
from pagination import Pagination

import simplejson as json
import functools


class RegionView(Pagination):
    async def fetch(self, current_page, page_size, sorter):
        region = Region(self.request.app.db_ref)
        total = await region.count()
        data_source = await region.fetch((current_page - 1) * page_size, page_size, sorter)
        return total, data_source

    async def remove(self, id):
        region = Region(self.request.app.db_ref)
        await region.remove(id)

    async def add(self, record):
        region = Region(self.request.app.db_ref)
        await region.add(record)

    async def update(self, record):
        region = Region(self.request.app.db_ref)
        await region.update(record)