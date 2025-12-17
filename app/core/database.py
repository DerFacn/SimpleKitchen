from quart import Quart, g
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database:
    """
    Database UoW (Unit of Work)  
    Provides all the functions for proper database connection and session management.
    """
    def __init__(self) -> None:
        self.Base = Base
            
    def init_app(self, app: Quart) -> None:
        self.app = app

        self.async_url = app.config.get("ASYNC_DATABASE_URL")
        self.sync_url = app.config.get("SYNC_DATABASE_URL")

        self.async_engine: AsyncEngine | None = None
        self.sync_engine: Engine | None = None

        self.AsyncSessionFactory = None
        self.SyncSessionFactory = None

        if self.async_url:
            self.async_engine = create_async_engine(
                self.async_url,
                echo=False,
                future=True,
            )
            self.AsyncSessionFactory = async_sessionmaker(
                bind=self.async_engine,
                expire_on_commit=False,
                class_=AsyncSession,
            )

        if self.sync_url:
            self.sync_engine = create_engine(
                self.sync_url,
                echo=False,
                future=True,
            )
            self.SyncSessionFactory = sessionmaker(
                bind=self.sync_engine,
                expire_on_commit=False,
                class_=Session,
            )

        self._register_hooks()

        @app.before_serving
        async def _init():
            await self.init_db()

    async def init_db(self):
        if self.async_engine:
            async with self.async_engine.begin() as conn:
                await conn.run_sync(self.Base.metadata.create_all)

        elif self.sync_engine:
            with self.sync_engine.begin() as conn:
                self.Base.metadata.create_all(bind=conn)

        else:
            raise RuntimeError(
                "No ASYNC_DATABASE_URL or SYNC_DATABASE_URL is provided. "
                "At least one database engine must be configured."
            )

    def _register_hooks(self):

        @self.app.before_request
        async def _open_session():
            if self.AsyncSessionFactory:
                g.session = self.AsyncSessionFactory()
            else:
                g.session = None

        @self.app.after_request
        async def _close_session(response):
            session = g.pop("session", None)
            if session:
                await session.close()
            return response

        @self.app.teardown_request
        async def _teardown(exc):
            session = g.pop("session", None)
            if session:
                await session.close()

    def get_async_session(self) -> AsyncSession:
        if not self.AsyncSessionFactory:
            raise RuntimeError("Async engine is not configured.")
        return self.AsyncSessionFactory()

    def get_sync_session(self) -> Session:
        if not self.SyncSessionFactory:
            raise RuntimeError("Sync engine is not configured.")
        return self.SyncSessionFactory()
