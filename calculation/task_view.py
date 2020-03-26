from aiohttp import web
from calculation.task import Task

import simplejson as json
import functools

class TaskView(web.View):
    async def get(self):
        task = Task(self.request.app.db_task)
        try:
            data_source = await task.fetch()
            return web.json_response(data_source, dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
        except:
            return web.Resource(status=400)
        
    
    async def post(self):
        task = Task(self.request.app.db_task)
        try:
            body = await self.request.json()
            method = body['method']
            if method == 'add':
                id = await task.add(body['PRODUCT'])
                await task.request(id, body)
            return await self.get()
        except:
            return web.Response(status=400)
