from aiohttp import web

import sys
import argparse
import simplejson as json
import functools
import sqlite3
import threading
import requests

from routes import routes

from calculation.task import Task
from calculation.task_update import TaskUpdate

ENGINE_ENDPOINT = "http://127.0.0.1:5000"

def tick(app):
    db_task = sqlite3.connect('./assets/task.db')
    task = Task(db_task, app.lock)
    rows = task.fetch_idle()

def initialize():
    try:
        app = web.Application()
        parser = argparse.ArgumentParser()
        parser.add_argument('--ee', help="engine endpoint")
        args = parser.parse_args()
        for route in routes:
            app.router.add_route(route[0], route[1], route[2])
        if args.ee == None:
            app.engine_endpoint = ENGINE_ENDPOINT
        else:
            app.engine_endpoint = args.ee
        app.db_ref = sqlite3.connect('./assets/ref.db')
        app.db_task = sqlite3.connect('./assets/task.db')
        cursor = app.db_task.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks("
            "id INTEGER PRIMARY KEY, "
            "product TEXT, "
            "createdAt timestamp, startedAt timestamp, finishedAt timestamp, percent INTEGER, status TEXT)")
        app.db_task.commit()
        app.lock = threading.Lock()
        app.task_update = TaskUpdate(app, 1.0, tick)
        app.task_update.start()
        return app
    except Exception as e:
        print('[ws]: could not initialize', str(e))
    
    
if __name__ == "__main__":
    app = initialize()
    web.run_app(app)
    app.task_update.stop()
