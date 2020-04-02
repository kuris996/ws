from calculation.task_view import TaskView
from calculation.kit_view import KitView

routes = [
    ('GET', '/api/kit', KitView),
    ('POST', '/api/kit', KitView),
    ('GET', '/api/task', TaskView),
    ('POST', '/api/task', TaskView)
]