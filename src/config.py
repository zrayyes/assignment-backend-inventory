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
