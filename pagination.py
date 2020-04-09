from aiohttp import web
import simplejson as json

import functools

class Pagination(web.View):
    async def get(self):
        page_size = int(self.request.query.get('pageSize', 10))
        current_page = int(self.request.query.get('currentPage', 1))
        sorter = self.request.query.get('sorter', None)
        if sorter != None:
            sorter = sorter.split('-')
            sorter = { "field" : sorter[0], "order" : sorter[1] }
        try: 
            total, data_source, filters = await self.fetch(
                current_page, page_size, sorter, self.request.query) 
            return web.json_response({
                'list': data_source,
                'pagination': { 
                    'total' : total,
                    'pageSize' : page_size,
                    'currentPage' : current_page
                },
                'filters' : filters
            }, dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
        except:
            return web.Response(status=400)

    async def post(self):
        try:
            body = await self.request.json()
            method = body['method']
            if (method == 'remove'):
                await self.remove(body['id'])
            elif (method == 'add'):
                await self.add(body)
            elif (method == 'update'):
                await self.update(body)
            return await self.get()
        except:
            return web.Response(status=400)