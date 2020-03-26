from database.fob_view import FobView
from calculation.task_view import TaskView


routes = [
    ('GET', '/api/fob', FobView),
    ('POST', '/api/fob', FobView),
    ('GET', '/api/task', TaskView),
    ('POST', '/api/task', TaskView)
]