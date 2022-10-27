import os
from contextvars import ContextVar

from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DevelopmentConfig, ProductionConfig


def create_app(args=None) -> Sanic:
    """Create and return Sanic application."""

    app = Sanic("StoreBackendApp")

    # Configuration
    if os.getenv("SANIC_ENV") == "development":
        app.update_config(DevelopmentConfig)
    else:
        app.update_config(ProductionConfig)

    # Database Setup & Middleware
    # https://sanic.dev/en/guide/how-to/orm.html#sqlalchemy
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)

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

    # Views
    from src.views.health_check import HealthCheckView

    app.add_route(HealthCheckView.as_view(), "/health_check")

    return app
