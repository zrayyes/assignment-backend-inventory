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

    from src.views.health_check import HealthCheckView

    app.add_route(HealthCheckView.as_view(), "/health_check")

    return app
