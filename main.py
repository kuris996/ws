from aiohttp import web

import json
import functools
import sqlite3

from database.fob_view import FobView
from database.fob import Fob
from routes import routes

def initialize():
    app = web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2])
    app.db = sqlite3.connect('../ref.db')
    return app


if __name__ == "__main__":
    web.run_app(initialize())
