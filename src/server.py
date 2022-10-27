from sanic import Sanic
import os
from sanic.response import text
from src.config import DevelopmentConfig, ProductionConfig


def create_app(args) -> Sanic:
    """Create and return Sanic application."""

    app = Sanic("StoreBackendApp")

    if os.getenv("SANIC_ENV") == "development":
        app.update_config(DevelopmentConfig)
    else:
        app.update_config(ProductionConfig)

    @app.get("/")
    async def hello(request):
        return text("OK!")

    return app
