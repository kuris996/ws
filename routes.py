from database.fob_view import FobView
from database.logistics_view import LogisticsView
from database.consignee_view import ConsigneeView
from database.region_view import RegionView
from database.perevalka_upakovka_view import PerevalkaUpakovkaView
from database.factory_view import FactoryView
from database.holding_view import HoldingView
from calculation.task_view import TaskView


routes = [
    ('GET', '/api/fob', FobView),
    ('POST', '/api/fob', FobView),
    ('GET', '/api/logistics', LogisticsView),
    ('POST', '/api/logistics', LogisticsView),
    ('GET', '/api/consignee', ConsigneeView),
    ('POST', '/api/consignee', ConsigneeView),
    ('GET', '/api/region', RegionView),
    ('POST', '/api/region', RegionView),
    ('GET', '/api/perevalka_upakovka', PerevalkaUpakovkaView),
    ('POST', '/api/perevalka_upakovka', PerevalkaUpakovkaView),
    ('GET', '/api/factory', FactoryView),
    ('POST', '/api/factory', FactoryView),
    ('GET', '/api/holding', HoldingView),
    ('POST', '/api/holding', HoldingView),
    ('GET', '/api/task', TaskView),
    ('POST', '/api/task', TaskView)
]