from aiohttp import web
import simplejson as json

import functools

class Pagination(web.View):
    async def get(self):
        page_size = 10
        if 'pageSize' in self.request.query:
            page_size = int(self.request.query['pageSize'])
        current_page = 1
        if 'currentPage' in self.request.query:
            current_page = int(self.request.query['currentPage'])
        sorter = None
        if 'sorter' in self.request.query:
            sorter = str(self.request.query['sorter'])
            sorter = sorter.split('-')
            sorter = { "field" : sorter[0], "order" : sorter[1] }
        try: 
            total, data_source = await self.fetch(current_page, page_size, sorter)
            return web.json_response({
                'list': data_source,
                'pagination': { 
                    'total' : total,
                    'pageSize' : page_size,
                    'currentPage' : current_page
                }
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