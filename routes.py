from calculation.task_view import TaskView
from calculation.kit_view import KitView
from calculation.input_view import InputView
from auth.login_view import LoginView

routes = [
    ('GET', '/api/login/account', LoginView),
    ('POST', '/api/login/account', LoginView),
    ('GET', '/api/kit', KitView),
    ('POST', '/api/kit', KitView),
    ('GET', '/api/task', TaskView),
    ('POST', '/api/task', TaskView),
    ('GET', '/api/input', InputView)
]