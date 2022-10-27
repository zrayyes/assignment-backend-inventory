from sanic.config import Config


class BaseConfig(Config):
    ...


class DevelopmentConfig(BaseConfig):
    ...


class TestingConfig(BaseConfig):
    ...


class ProductionConfig(BaseConfig):
    ...
