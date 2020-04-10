from aiohttp import web
import simplejson as json

import functools

class LoginView(web.View):
    async def post(self):
        try:
            body = await self.request.json()
            if body['password'] == 'qwerty1@3' and body['userName'] == 'user':
                return web.json_response({
                    "status": 'ok',
                    "currentAuthority": 'user'
                }, dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
            else:
                return web.json_response({
                    "status": 'error',
                    "currentAuthority": 'guest'
                }, dumps=functools.partial(json.dumps, indent=4, ensure_ascii=False, encoding='utf8'))
        except:
            return web.Response(status=403)