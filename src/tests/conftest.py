import os

import pytest

from src.server import create_app


@pytest.fixture(scope="module")
def app():
    os.environ["SANIC_ENV"] = "testing"
    sanic_app = create_app()

    return sanic_app


@pytest.fixture(scope="function")
def db():
    ...
