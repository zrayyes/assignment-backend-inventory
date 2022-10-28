import datetime

from sqlalchemy import insert, select

from src.models import Base, Item, ItemType, Space


async def setup_db(app):

    async with app.ctx.db_engine.begin() as conn:
        if app.ctx.CONFIG.RECREATE_TABLES:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        if app.ctx.CONFIG.SEED_DB:
            # Storage Spaces
            await conn.execute(
                insert(Space).values(name="Big", capacity=100, is_refrigerated=True)
            )
            await conn.execute(
                insert(Space).values(name="Small", capacity=5, is_refrigerated=False)
            )

            # Item Types
            await conn.execute(
                insert(ItemType).values(name="Vanilla Ice Cream", needs_fridge=True)
            )
            await conn.execute(
                insert(ItemType).values(name="Pink Socks", needs_fridge=False)
            )

            # Fetch IDs for Spaces and Item Types
            big_storage = await conn.execute(select(Space).where(Space.name == "Big"))
            big_storage = big_storage.first()
            small_storage = await conn.execute(
                select(Space).where(Space.name == "Small")
            )
            small_storage = small_storage.first()

            vanilla_icecream = await conn.execute(
                select(ItemType).where(ItemType.name == "Vanilla Ice Cream")
            )
            vanilla_icecream = vanilla_icecream.first()
            pink_socks = await conn.execute(
                select(ItemType).where(ItemType.name == "Pink Socks")
            )
            pink_socks = pink_socks.first()

            # Add items
            await conn.execute(
                insert(Item).values(
                    expiry_date=datetime.date.today() + datetime.timedelta(days=1),
                    storage_space_id=big_storage.id,
                    item_type_id=vanilla_icecream.id,
                )
            )

            await conn.execute(
                insert(Item).values(
                    expiry_date=datetime.date.today()
                    + datetime.timedelta(days=365 * 100),
                    storage_space_id=small_storage.id,
                    item_type_id=pink_socks.id,
                )
            )
