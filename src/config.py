import os

from sanic.config import Config


class BaseConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite+aiosqlite:///store.db"
    )


class DevelopmentConfig(BaseConfig):
    ...


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"


class ProductionConfig(BaseConfig):
    ...


AppConfig = ProductionConfig()
if os.getenv("SANIC_ENV") == "development":
    AppConfig = DevelopmentConfig()
if os.getenv("SANIC_ENV") == "testing":
    AppConfig = TestingConfig()
