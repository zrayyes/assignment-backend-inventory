from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import AppConfig

async_engine = create_async_engine(
    AppConfig.SQLALCHEMY_DATABASE_URI, echo=True, future=True
)


async def get_async_session():
    return sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
