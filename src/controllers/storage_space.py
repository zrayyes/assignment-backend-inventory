from typing import List, Optional

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Item, Space


async def get_storage_space_by_id(session: AsyncSession, id: int) -> Optional[Space]:
    stmt = select(Space).where(Space.id == id)
    result = await session.execute(stmt)
    space = result.scalar()
    return space


async def get_storage_space_usage(session: AsyncSession, space: Space) -> int:
    stmt = (
        select(func.count())
        .select_from(Space)
        .join(Space.items)
        .where(Space.id == space.id)
    )
    result = await session.execute(stmt)
    usage_count = result.scalar()
    return usage_count


async def get_all_items_for_storage_space(
    session: AsyncSession,
    storage_space_id: int,
    sort_direction: Optional[str] = None,
    count=None,
    offset=0,
) -> List[Item]:

    sort_by = None
    if sort_direction == "ASC":
        sort_by = Item.expiry_date
    if sort_direction == "DESC":
        sort_by = Item.expiry_date.desc()

    statement = (
        select(Item)
        .where(Item.storage_space_id == storage_space_id)
        .options(selectinload(Item.storage_space))
        .options(selectinload(Item.item_type))
        .order_by(sort_by)
        .offset(offset)
        .limit(count)
    )

    result = await session.execute(statement)
    return result.scalars().all()


async def update_storage_space(session: AsyncSession, space: Space, **kwargs) -> Space:
    if "name" in kwargs:
        space.name = kwargs["name"]
    await session.commit()


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


async def delete_storage_space(session: AsyncSession, id: int):
    await session.execute(delete(Space).where(Space.id == id))
    await session.commit()
