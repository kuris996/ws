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
import simplejson as json
from collections import defaultdict

from routes import routes

from calculation.task import Task
from calculation.kit import Kit
from calculation.backtesting import Backtesting
from bucket import Bucket
from ticker import Ticker

from constants import *

def check_results(app):
    try:
        bucket = app.bucket
        req = requests.post(app.engine_endpoint + "/check_results")
        result = json.loads(req.text)
        db = sqlite3.connect(DB_PATH)
        save_db = False
        for key in result:
            value = result[key]
            startedAt = None
            finishedAt = None
            _type = None
            if value['startedAt'] != None:
                startedAt = dateutil.parser.isoparse(value['startedAt'])
            if value['finishedAt'] != None:
                finishedAt  = dateutil.parser.isoparse(value['finishedAt'])
            if value['type'] != None:
                _type = value['type']
            record = {
                "id" : key,
                "startedAt" : startedAt,
                "finishedAt" : finishedAt,
                "status" : value['status']
            }
            if _type == 'model_calculation':
                task = Task(db, app.db_lock)
                task.update_status(record)
                save_db = True
            elif _type == 'generate_inputs':
                kit = Kit(db, app.db_lock)
                kit.update_status(record)
                save_db = True
            elif _type == 'backtesting':
                backtesting = Backtesting(db, app.db_lock)
                backtesting.update_status(record)
                save_db = True

        if save_db:
            bucket.write(DB_PATH, DB_PATH)
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
        print("ENDPOINT: ", app.engine_endpoint)
        bucket = Bucket()
        bucket.read(DB_PATH, DB_PATH)
        app.bucket = bucket
        app.db = sqlite3.connect(DB_PATH)
        cursor = app.db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS task("
            "id INTEGER PRIMARY KEY, "
            "uuid TEXT, kit TEXT, product TEXT, kitName TEXT, createdAt TIMESTAMP, startedAt TIMESTAMP, finishedAt TIMESTAMP, status TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS kit("
            "id INTEGER PRIMARY KEY, "
            "uuid TEXT, name TEXT, createdAt TIMESTAMP, startedAt TIMESTAMP, finishedAt TIMESTAMP, status TEXT)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS backtesting("
            "id INTEGER PRIMARY KEY, "
            "createdAt TIMESTAMP, startedAt TIMESTAMP, finishedAt TIMESTAMP, status TEXT)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS backtesting_task("
            "id INTEGER PRIMARY KEY,"
            "backtestingId INTEGER, taskId INTEGER)"
        )
        app.db.commit()
        app.db_lock = threading.Lock()
        app.task_update = Ticker(app, 5.0, check_results)
        app.task_update.start()
        return app
    except Exception as e:
        print('[ws]: could not initialize', str(e))
      

if __name__ == "__main__":
    app = initialize()
    web.run_app(app)
    app.task_update.stop()
