from aiohttp import web

import argparse
import json
import functools
import sqlite3
import threading

from database.fob_view import FobView
from database.fob import Fob
from routes import routes

from calculation.task import Task
from calculation.task_update import TaskUpdate

def tick(app):
    db_task = sqlite3.connect('./assets/task.db')
    task = Task(db_task, app.lock)
    rows = task.fetch_idle()

def initialize():
    app = web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2])
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


if __name__ == "__main__":
    app = initialize()
    web.run_app(app)
    app.task_update.stop()
