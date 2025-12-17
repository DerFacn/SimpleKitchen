import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GenericKey'
    ASYNC_DATABASE_URL = os.environ.get('ASYNC_DATABASE_URL')
    SYNC_DATABASE_URL = os.environ.get('SYNC_DATABASE_URL')
