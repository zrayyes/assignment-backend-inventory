import pytest

from src.db import get_async_session
from src.helpers import date_after_n_days
from src.models import Item, ItemType, Space


@pytest.mark.asyncio
async def test_model_relationships(app):
    async_session = await get_async_session()

    async with async_session() as session:
        # Items
        item_1 = Item(expiry_date=date_after_n_days(1))
        item_2 = Item(expiry_date=date_after_n_days(1))

        # Storage Space
        space = Space(
            name="MYSPACE", capacity=100, is_refrigerated=True, items=[item_1, item_2]
        )

        # Item Types
        item_type_1 = ItemType(name="TYPE1", needs_fridge=True, items=[item_1])
        item_type_2 = ItemType(name="TYPE2", needs_fridge=True, items=[item_2])

        # Add
        session.add_all(
            [
                space,
                item_type_1,
                item_type_2,
                item_1,
                item_2,
            ]
        )

        await session.flush()

        # Check Relationships
        assert item_1 in space.items
        assert item_2 in space.items

        assert item_1 in item_type_1.items
        assert item_2 in item_type_2.items

        # Check Foreign Keys
        item_1_db = await session.get(Item, item_1.id)
        assert item_1_db.storage_space_id == space.id
        assert item_1_db.item_type_id == item_type_1.id

        item_2_db = await session.get(Item, item_2.id)
        assert item_2_db.storage_space_id == space.id
        assert item_2_db.item_type_id == item_type_2.id
