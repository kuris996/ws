from calculation.task_view import TaskView


routes = [
    ('GET', '/api/task', TaskView),
    ('POST', '/api/task', TaskView)
]