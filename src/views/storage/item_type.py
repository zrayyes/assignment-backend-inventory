from dataclasses import dataclass

from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from src.controllers.item_type import (create_item_type, get_item_type_by_id,
                                       get_item_type_by_name, update_item_type)
from src.db import get_async_session


@dataclass
class ItemTypeIn:
    name: str
    needs_fridge: bool


@dataclass
class ItemTypeUpdate:
    name: str


class SingleItemTypeView(HTTPMethodView):
    async def get(self, request, id):
        async_session = await get_async_session()

        async with async_session() as session:
            item_type = await get_item_type_by_id(session, id)

            if not item_type:
                raise SanicException("Item type does not exist.", status_code=404)

        return json(item_type.to_dict())

    @validate(json=ItemTypeUpdate)
    async def patch(self, request, id, body: ItemTypeUpdate):
        async_session = await get_async_session()

        async with async_session() as session:
            item_type = await get_item_type_by_id(session, id)

            if not item_type:
                raise SanicException("Item type does not exist.", status_code=404)

            item_type_with_same_name = await get_item_type_by_name(session, body.name)
            if item_type_with_same_name:
                if item_type_with_same_name.id != id:
                    raise SanicException(
                        f"Item type with same name already exists. ItemType = {item_type_with_same_name.id}",
                        status_code=403,
                    )

            update = {}
            update["name"] = body.name

            await update_item_type(session, item_type, **update)

        return json(item_type.to_dict())

    async def delete(self, request, id):
        pass


class ItemTypeView(HTTPMethodView):
    @validate(json=ItemTypeIn)
    async def post(self, request, body: ItemTypeIn):
        async_session = await get_async_session()
        async with async_session() as session:

            item_type = await get_item_type_by_name(session, body.name)

            if item_type:
                raise SanicException(
                    f"Item type with same name already exists. ItemType = {item_type.id}",
                    status_code=403,
                )

            item_type = await create_item_type(
                session,
                name=body.name,
                needs_fridge=body.needs_fridge,
            )
        return json(item_type.to_dict())


item_type_blueprint = Blueprint("item_type")
item_type_blueprint.add_route(ItemTypeView.as_view(), "/item_type")
item_type_blueprint.add_route(SingleItemTypeView.as_view(), "/item_type/<id:int>")
