from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Item, Space


async def get_storage_space_by_id(session: AsyncSession, id: int) -> Optional[Space]:
    stmt = select(Space).where(Space.id == id)
    result = await session.execute(stmt)
    space = result.scalar()
    return space


async def get_all_items_for_storage_space(
    session: AsyncSession, storage_space_id: int
) -> List[Item]:
    statement = (
        select(Item)
        .where(Item.storage_space_id == storage_space_id)
        .options(selectinload(Item.storage_space))
        .options(selectinload(Item.item_type))
    )
    result = await session.execute(statement)
    return result.scalars().all()


async def create_storage_space(
    session: AsyncSession, name: str, capacity: int, is_refrigerated: bool
) -> Space:
    space = Space(
        name=name,
        capacity=capacity,
        is_refrigerated=is_refrigerated,
    )
    session.add(space)
    await session.commit()
    return space
