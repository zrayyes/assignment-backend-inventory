import asyncio
import os
from uuid import uuid4

import pytest
import pytest_asyncio
from sanic_testing import TestManager
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.controllers.storage_space import create_storage_space
from src.db import async_engine, get_async_session
from src.helpers import date_after_n_days
from src.models import Base, Item, ItemType
from src.server import create_app


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
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
            space = await create_storage_space(session, name, capacity, is_refrigerated)
        return space

    return _add_storage_space


@pytest_asyncio.fixture(scope="function")
async def add_item_type():
    async def _add_item_type(name=None, needs_fridge=False):
        if not name:
            name = str(uuid4())

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

            # Fetch relationships
            statement = (
                select(Item)
                .where(Item.id == item.id)
                .options(selectinload(Item.storage_space))
                .options(selectinload(Item.item_type))
            )
            result = await session.execute(statement)
            item = result.scalars().first()

        return item

    return _add_item
