from database.fob_view import FobView

routes = [
    ('GET', '/api/fob', FobView),
    ('POST', '/api/fob', FobView)
]