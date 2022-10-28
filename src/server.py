import os
from contextvars import ContextVar

from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DevelopmentConfig, ProductionConfig, TestingConfig


async def setup_db(app):
    from src.models import Base

    async with app.ctx.db_engine.begin() as conn:
        if app.ctx.CONFIG.RECREATE_TABLES:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        if app.ctx.CONFIG.SEED_DB:
            ...


def create_app(args=None) -> Sanic:
    """Create and return Sanic application."""

    app = Sanic("StoreBackendApp")

    # Configuration
    AppConfig = ProductionConfig()
    if os.getenv("SANIC_ENV") == "development":
        AppConfig = DevelopmentConfig()
    if os.getenv("SANIC_ENV") == "testing":
        AppConfig = TestingConfig()

    app.ctx.CONFIG = AppConfig
    app.update_config(AppConfig)

    # Database Setup & Middleware
    # https://sanic.dev/en/guide/how-to/orm.html#sqlalchemy
    engine = create_async_engine(AppConfig.SQLALCHEMY_DATABASE_URI, echo=True)

    app.ctx.db_engine = engine

    _sessionmaker = sessionmaker(engine, AsyncSession, expire_on_commit=False)

    _base_model_session_ctx = ContextVar("session")

    @app.middleware("request")
    async def inject_session(request):
        request.ctx.session = _sessionmaker()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

    @app.middleware("response")
    async def close_session(request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()

    app.register_listener(setup_db, "before_server_start")

    # Views
    from src.views.health_check import HealthCheckView

    app.add_route(HealthCheckView.as_view(), "/health_check")

    return app
