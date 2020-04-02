from aiohttp import web
from calculation.input import Input

import simplejson as json
import functools

class InputView(web.View):
    async def get(self):
        try:
            prefix = str(self.request.query.get('prefix', ""))
            if prefix and not prefix.endswith('/'):
                prefix += '/'
            input = Input()
            data_source = input.fetch(prefix)
            return web.json_response(
                data_source
            , dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
        except Exception as e:
            return web.Response(status=400)
