from sanic.config import Config
import os

class BaseConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    ...


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    ...
