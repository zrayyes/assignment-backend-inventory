import asyncio
import os

import pytest
import pytest_asyncio
from sanic_testing import TestManager

from src.db import async_engine, get_async_session
from src.helpers import date_after_n_days
from src.models import Base, Item, ItemType, Space
from src.server import create_app


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
def app():
    os.environ["SANIC_ENV"] = "testing"
    app = create_app()
    TestManager(app)
    asyncio.run(create_tables())

    return app


@pytest_asyncio.fixture(scope="function")
async def add_storage_space():
    async def _add_storage_space(name, capacity, is_refrigerated):
        async_session = await get_async_session()

        async with async_session() as session:
            # TODO: Move to controller
            space = Space(name=name, capacity=capacity, is_refrigerated=is_refrigerated)
            session.add(space)
            await session.commit()
        return space

    return _add_storage_space


@pytest_asyncio.fixture(scope="function")
async def add_item_type():
    async def _add_item_type(name, needs_fridge):
        async_session = await get_async_session()

        async with async_session() as session:
            # TODO: Move to controller
            item_type = ItemType(name=name, needs_fridge=needs_fridge)
            session.add(item_type)
            await session.commit()
        return item_type

    return _add_item_type


@pytest_asyncio.fixture(scope="function")
async def add_item():
    async def _add_item(
        storage_space,
        item_type,
        expiry_date=date_after_n_days(1),
    ):
        async_session = await get_async_session()

        async with async_session() as session:
            # TODO: Move to controller
            item = Item(
                storage_space_id=storage_space.id,
                item_type_id=item_type.id,
                expiry_date=expiry_date,
            )
            session.add(item)
            await session.commit()
        return item

    return _add_item
