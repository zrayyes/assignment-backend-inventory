import datetime

import pytest

from src.models import Item, ItemType, Space


@pytest.mark.asyncio
async def test_model_relationships(db_session):
    # Items
    item_1 = Item(expiry_date=datetime.date.today() + datetime.timedelta(days=1))
    item_2 = Item(expiry_date=datetime.date.today() + datetime.timedelta(days=2))

    # Storage Space
    space = Space(
        name="MYSPACE", capacity=100, is_refrigerated=True, items=[item_1, item_2]
    )

    # Item Types
    item_type_1 = ItemType(name="TYPE1", needs_fridge=True, items=[item_1])
    item_type_2 = ItemType(name="TYPE2", needs_fridge=True, items=[item_2])

    # Add
    db_session.add_all(
        [
            space,
            item_type_1,
            item_type_2,
            item_1,
            item_2,
        ]
    )

    # Check Relationships
    assert item_1 in space.items
    assert item_2 in space.items

    assert item_1 in item_type_1.items
    assert item_2 in item_type_2.items
