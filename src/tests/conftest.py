import pytest

from src.server import create_app


@pytest.fixture(scope="module")
def app():
    sanic_app = create_app()

    return sanic_app


@pytest.fixture(scope="function")
def db():
    ...
