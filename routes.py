from calculation.task_view import TaskView
from calculation.kit_view import KitView
from calculation.backtesting_view import BacktestingView
from calculation.input_view import InputView
from calculation.params_view import ParamsView
from auth.login_view import LoginView

routes = [
    ('GET', '/api/login/account', LoginView),
    ('POST', '/api/login/account', LoginView),
    ('GET', '/api/kit', KitView),
    ('POST', '/api/kit', KitView),
    ('GET', '/api/task', TaskView),
    ('POST', '/api/task', TaskView),
    ('GET', '/api/backtesting', BacktestingView),
    ('POST', '/api/backtesting', BacktestingView),
    ('GET', '/api/input', InputView),
    ('GET', '/api/params', ParamsView)
]