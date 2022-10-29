from dataclasses import dataclass

from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.db import get_async_session
from src.models import Item, Space


class SingleStorageSpaceView(HTTPMethodView):
    async def get(self, request, id):
        async_session = await get_async_session()

        async with async_session() as session:
            stmt = select(Space).where(Space.id == id)
            result = await session.execute(stmt)
            space = result.scalar()

            if not space:
                raise SanicException("Storage space does not exist.", status_code=404)

            items = []

            statement = (
                select(Item)
                .where(Item.storage_space_id == id)
                .options(selectinload(Item.storage_space))
                .options(selectinload(Item.item_type))
            )
            result = await session.execute(statement)
            for item in result.scalars().all():
                items.append(item.to_dict())

        output = space.to_dict()
        output["items"] = items
        return json(output)


@dataclass
class StorageSpaceIn:
    name: str
    capacity: int
    is_refrigerated: bool


class StorageSpaceView(HTTPMethodView):
    @validate(json=StorageSpaceIn)
    async def post(self, request, body: StorageSpaceIn):
        if body.capacity < 0:
            raise SanicException(
                "Storage space cannot have capacity less than 0.", status_code=400
            )
        async_session = await get_async_session()
        async with async_session() as session:
            space = Space(
                name=body.name,
                capacity=body.capacity,
                is_refrigerated=body.is_refrigerated,
            )
            session.add(space)
            await session.commit()
        return json(space.to_dict())


storage_space_blueprint = Blueprint("storage_space")
storage_space_blueprint.add_route(StorageSpaceView.as_view(), "/space")
storage_space_blueprint.add_route(SingleStorageSpaceView.as_view(), "/space/<id:int>")
