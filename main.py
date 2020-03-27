from aiohttp import web

import json
import functools
import sqlite3

from database.fob_view import FobView
from database.fob import Fob
from routes import routes

from calculation.task import Task
from calculation.task_update import TaskUpdate

def tick():
    db_task = sqlite3.connect('../task.db')
    task = Task(db_task)
    rows = task.fetch_idle()
    print(rows)

def initialize():
    app = web.Application()
    for route in routes:
        app.router.add_route(route[0], route[1], route[2])
    app.db_ref = sqlite3.connect('../ref.db')
    app.db_task = sqlite3.connect('../task.db')
    cursor = app.db_task.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS tasks("
        "id INTEGER PRIMARY KEY, "
        "product TEXT, "
        "createdAt timestamp, startedAt timestamp, finishedAt timestamp, percent INTEGER, status TEXT)")
    app.db_task.commit()
    app.task_update = TaskUpdate(1.0, tick)
    app.task_update.start()
    return app


if __name__ == "__main__":
    app = initialize()
    web.run_app(app)
    app.task_update.stop()
