import os

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import TestingConfig
from src.models import Base
from src.server import create_app


async def drop_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def app():
    os.environ["SANIC_ENV"] = "testing"
    sanic_app = create_app()

    _sessionmaker = sessionmaker(sanic_app.ctx.db_engine, AsyncSession)

    # TODO: Refactor?
    async with _sessionmaker():
        async with sanic_app.ctx.db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield sanic_app

    await drop_tables(sanic_app.ctx.db_engine)


@pytest_asyncio.fixture(scope="function")
async def db_session():

    engine = create_async_engine(TestingConfig.SQLALCHEMY_DATABASE_URI)
    _sessionmaker = sessionmaker(engine, AsyncSession)

    async with _sessionmaker() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    await drop_tables(engine)
