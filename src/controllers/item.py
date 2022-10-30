from datetime import date
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.controllers.storage_space import get_storage_space_usage
from src.models import Item, ItemType, Space


class ExpiredDate(Exception):
    pass


class StorageSpaceFull(Exception):
    pass


class IncompatibleStorageSpace(Exception):
    pass


async def get_item_by_id(session: AsyncSession, id: int) -> Optional[Item]:
    stmt = (
        select(Item)
        .where(Item.id == id)
        .options(selectinload(Item.item_type))
        .options(selectinload(Item.storage_space))
    )
    result = await session.execute(stmt)
    item = result.scalar()
    return item


async def delete_item(session: AsyncSession, id: int):
    await session.execute(delete(Item).where(Item.id == id))
    await session.commit()


async def create_item(
    session: AsyncSession, space: Space, item_type: ItemType, expiry_date: date
) -> Item:
    # Check if date in the past
    if expiry_date <= date.today():
        raise ExpiredDate()

    # Check if storage is incompatible
    if space.is_refrigerated is not item_type.needs_fridge:
        raise IncompatibleStorageSpace()

    # Check if storage space full
    storage_usage_count = await get_storage_space_usage(session, space)
    if space.capacity <= storage_usage_count:
        raise StorageSpaceFull()

    item = Item(
        expiry_date=expiry_date,
        storage_space_id=space.id,
        item_type_id=item_type.id,
    )
    session.add(item)
    await session.commit()
    item.storage_space
    item.item_type
    return item
