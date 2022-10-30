from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Item, ItemType


async def create_item_type(
    session: AsyncSession, name: str, needs_fridge: bool
) -> ItemType:
    item_type = ItemType(
        name=name,
        needs_fridge=needs_fridge,
    )
    session.add(item_type)
    await session.commit()
    return item_type


async def get_item_type_by_id(session: AsyncSession, id: int) -> Optional[ItemType]:
    stmt = select(ItemType).where(ItemType.id == id)
    result = await session.execute(stmt)
    item_type = result.scalar()
    return item_type


async def get_item_type_by_name(session: AsyncSession, name: str) -> Optional[ItemType]:
    stmt = select(ItemType).where(ItemType.name == name)
    result = await session.execute(stmt)
    item_type = result.scalar()
    return item_type


async def update_item_type(session: AsyncSession, item_type: ItemType, **kwargs):
    if "name" in kwargs:
        item_type.name = kwargs["name"]
    await session.commit()


async def get_all_items_for_item_type(
    session: AsyncSession,
    item_type_id: int,
    count=None,
) -> List[Item]:

    statement = (
        select(Item)
        .where(Item.item_type_id == item_type_id)
        .options(selectinload(Item.storage_space))
        .options(selectinload(Item.item_type))
        .limit(count)
    )

    result = await session.execute(statement)
    return result.scalars().all()


async def delete_item_type(session: AsyncSession, id: int):
    await session.execute(delete(ItemType).where(ItemType.id == id))
    await session.commit()
