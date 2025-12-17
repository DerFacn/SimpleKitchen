from quart import Quart
from app.config import Config
from app.core.database import Database

db = Database()


def create_app(config_obj=Config):
    app = Quart(__name__)
    app.config.from_object(config_obj)
    
    db.init_app(app)
    
    @app.route('/')
    async def index():
        return {"message": "Hello World"}
    
    return app
