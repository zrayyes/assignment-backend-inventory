from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Item


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
