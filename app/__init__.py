from quart import Quart, request
from app.config import Config
from app.core.database import Database

db = Database()


def create_app(config_obj=Config):
    app = Quart(__name__)
    app.config.from_object(config_obj)
    
    db.init_app(app)
    
    from app import models
    
    @app.before_serving
    async def before_serving():
        await db.init_db()
    
    @app.route('/')
    async def index():
        client_addr = request.headers.get('X-Real-IP')
        return {"message": "Hello World", "remote_addr": client_addr if client_addr else request.remote_addr}
    
    return app
