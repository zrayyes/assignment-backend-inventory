from sanic import Blueprint
from sanic.response import json
from sanic.views import HTTPMethodView
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models import Item


class SingleStorageSpaceView(HTTPMethodView):
    async def get(self, request, id):
        session = request.ctx.session
        items = []
        async with session.begin():
            statement = (
                select(Item)
                .where(Item.storage_space_id == id)
                .options(selectinload(Item.storage_space))
                .options(selectinload(Item.item_type))
            )
            result = await session.execute(statement)
            for item in result.scalars().all():
                items.append(item.to_dict())
        return json({"items": items})


class StorageSpaceView(HTTPMethodView):
    async def get(self, request):
        ...

    async def post(self, request):
        ...


storage_space_blueprint = Blueprint("storage_space")
storage_space_blueprint.add_route(StorageSpaceView.as_view(), "/space")
storage_space_blueprint.add_route(SingleStorageSpaceView.as_view(), "/space/<id:int>")
