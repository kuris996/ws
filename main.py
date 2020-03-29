from aiohttp import web

import sys
import os
import argparse
import simplejson as json
import functools
import sqlite3
import threading
import requests
import datetime
import dateutil.parser

from routes import routes

from calculation.task import Task
from calculation.task_update import TaskUpdate

ENGINE_ENDPOINT = "http://127.0.0.1:5000"

def tick(app):
    try:
        headers = {'Content-type': 'application/json'}
        req = requests.post(app.engine_endpoint + "/check_results")
        result = json.loads(req.text)
        db_task = sqlite3.connect('./assets/task.db')
        task = Task(db_task, app.lock)
        for key in result:
            value = result[key]
            startedAt = None
            finishedAt = None
            if value['startedAt'] != None:
                startedAt = dateutil.parser.isoparse(value['startedAt'])
            if value['finishedAt'] != None:
                finishedAt  = dateutil.parser.isoparse(value['finishedAt'])
            record = {
                "id" : key,
                "startedAt" : startedAt,
                "finishedAt" : finishedAt,
                "status" : value['status']
            }
            task.update_status(record)
    except Exception as e:
        print('[tick]: ', e)



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
        app.task_update = TaskUpdate(app, 5.0, tick)
        app.task_update.start()
        return app
    except Exception as e:
        print('[ws]: could not initialize', str(e))
    
    
if __name__ == "__main__":
    app = initialize()
    web.run_app(app)
    app.task_update.stop()
