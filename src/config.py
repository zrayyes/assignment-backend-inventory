import os

from sanic.config import Config


class BaseConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "RECREATE_TABLES", "sqlite+aiosqlite:///:memory:"
    )
    RECREATE_TABLES = os.environ.get("RECREATE_TABLES", False) is True
    SEED_DB = os.environ.get("SEED_DB", False) is True


class DevelopmentConfig(BaseConfig):
    RECREATE_TABLES = True
    SEED_DB = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"


class ProductionConfig(BaseConfig):
    ...
