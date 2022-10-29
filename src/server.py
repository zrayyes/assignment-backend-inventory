from sanic import Sanic

from src.config import AppConfig


def create_app(args=None) -> Sanic:
    """Create and return Sanic application."""

    app = Sanic("StoreBackendApp", config=AppConfig)

    # Views
    from src.views import storage_blueprint
    from src.views.health_check import HealthCheckView

    app.add_route(HealthCheckView.as_view(), "/health_check")
    app.blueprint(storage_blueprint)

    return app
