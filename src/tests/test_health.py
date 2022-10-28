import os


def test_health_check(app):
    _, response = app.test_client.get("/health_check")

    assert response.status == 200
    assert response.json["status"] == "success"


def test_app_config(app):
    from src.config import TestingConfig

    AppConfig = app.ctx.CONFIG
    assert os.getenv("SANIC_ENV") == "testing"
    assert type(AppConfig) == TestingConfig
    assert AppConfig.TESTING == True
