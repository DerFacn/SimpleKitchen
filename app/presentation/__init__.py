from quart import Quart
from .routes import index


def register_routes(app: Quart) -> None:
    app.add_url_rule('/', 'index', index, methods=['GET'])
