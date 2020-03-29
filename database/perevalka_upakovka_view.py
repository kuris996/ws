from aiohttp import web
from database.perevalka_upakovka import PerevalkaUpakovka
from pagination import Pagination

import simplejson as json
import functools


class PerevalkaUpakovkaView(Pagination):
    async def fetch(self, current_page, page_size, sorter):
        perevalka_upakovka = PerevalkaUpakovka(self.request.app.db_ref)
        total = await perevalka_upakovka.count()
        data_source = await perevalka_upakovka.fetch((current_page - 1) * page_size, page_size, sorter)
        return total, data_source

    async def remove(self, id):
        perevalka_upakovka = PerevalkaUpakovka(self.request.app.db_ref)
        await perevalka_upakovka.remove(id)

    async def add(self, record):
        perevalka_upakovka = PerevalkaUpakovka(self.request.app.db_ref)
        await perevalka_upakovka.add(record)

    async def update(self, record):
        perevalka_upakovka = PerevalkaUpakovka(self.request.app.db_ref)
        await perevalka_upakovka.update(record)