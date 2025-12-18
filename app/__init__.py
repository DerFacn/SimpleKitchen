from quart import Quart, request
from app.config import Config
from app.core.database import Database

db = Database()


def create_app(config_obj=Config):
    app = Quart(__name__)
    app.config.from_object(config_obj)
    
    db.init_app(app)
    
    app.jinja_env.cache = {}
    app.jinja_env.auto_reload = True
    
    from app import models
    from app.presentation import register_routes
    
    @app.before_serving
    async def before_serving():
        await db.init_db()
        
    register_routes(app)
    
    return app
