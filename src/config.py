from sanic.config import Config


class BaseConfig(Config):
    TESTING = False


class DevelopmentConfig(BaseConfig):
    ...


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    ...
