from aiohttp import web
from calculation.bucket import Bucket

import simplejson as json
import functools

class InputView(web.View):
    async def get(self):
        try:
            kit = str(self.request.query.get('kit', ""))
            uuid = str(self.request.query.get('uuid', ""))
            bucket = Bucket()
            data_source = bucket.fetch(kit, uuid)
            return web.json_response(
                data_source
            , dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
        except:
            return web.Response(status=400)
