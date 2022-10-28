import os

import pytest


@pytest.mark.asyncio
async def test_health_check(app):
    _, response = await app.asgi_client.get("/health_check")

    assert response.status == 200
    assert response.json["status"] == "success"


@pytest.mark.asyncio
async def test_app_config(app):
    from src.config import TestingConfig

    AppConfig = app.ctx.CONFIG
    assert os.getenv("SANIC_ENV") == "testing"
    assert type(AppConfig) == TestingConfig
    assert AppConfig.TESTING is True
