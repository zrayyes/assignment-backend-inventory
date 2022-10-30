from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ItemType


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


async def get_item_type_by_name(session: AsyncSession, name: str) -> Optional[ItemType]:
    stmt = select(ItemType).where(ItemType.name == name)
    result = await session.execute(stmt)
    item_type = result.scalar()
    return item_type
