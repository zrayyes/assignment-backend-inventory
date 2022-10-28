import os

from sanic.config import Config


class BaseConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"
    RECREATE_TABLES = os.environ.get("RECREATE_TABLES", False)
    SEED_DB = os.environ.get("SEED_DB", False)


class DevelopmentConfig(BaseConfig):
    RECREATE_TABLES = True
    SEED_DB = True


class TestingConfig(BaseConfig):
    TESTING = True
    RECREATE_TABLES = True


class ProductionConfig(BaseConfig):
    ...
