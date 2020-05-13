from aiohttp import web
from bucket import Bucket

import simplejson as json
import functools

class ParamsView(web.View):
    async def get(self):
        try:
            kit = str(self.request.query.get('kit', ""))
            bucket = self.request.app.bucket
            data_source = bucket.fetch_inputs(kit)
            products = []
            for product in data_source:
                for a in product['children']:
                    if a['name'] != 'railway':
                        continue
                    years = []
                    for b in a['children']:
                        years.append(b['name'])
                    products.append({
                        'product' : product['name'],
                        'years' : years
                    })
            return web.json_response(
                products
            , dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
        except:
            return web.Response(status=400)