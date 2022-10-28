import os

import pytest
import pytest_asyncio

from src.server import create_app


@pytest.fixture(scope="module")
def app():
    os.environ["SANIC_ENV"] = "testing"
    sanic_app = create_app()

    return sanic_app


@pytest_asyncio.fixture(scope="function")
async def db_session():
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    from src.config import TestingConfig
    from src.models import Base

    engine = create_async_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
    _sessionmaker = sessionmaker(engine, AsyncSession)

    async with _sessionmaker() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
