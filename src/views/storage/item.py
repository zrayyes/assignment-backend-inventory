from dataclasses import dataclass

from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from src.controllers.item import (ExpiredDate, create_item, delete_item,
                                  get_item_by_id)
from src.controllers.item_type import get_item_type_by_id
from src.controllers.storage_space import get_storage_space_by_id
from src.db import get_async_session
from src.helpers import format_str_to_date


@dataclass
class NewItemIn:
    expiry_date: str
    storage_space_id: int
    item_type_id: int


class ItemView(HTTPMethodView):
    @validate(json=NewItemIn)
    async def post(self, request, body: NewItemIn):
        async_session = await get_async_session()

        async with async_session() as session:
            # Validate date
            try:
                expiry_date = format_str_to_date(body.expiry_date)
            except ValueError:
                raise SanicException("Invalid date format", status_code=403)

            # validate storage
            space = await get_storage_space_by_id(session, body.storage_space_id)

            if not space:
                raise SanicException("Storage space does not exist.", status_code=404)

            # validate item type
            item_type = await get_item_type_by_id(session, body.item_type_id)

            if not item_type:
                raise SanicException("Item type does not exist.", status_code=404)

            try:
                item = await create_item(session, space, item_type, expiry_date)
            except ExpiredDate:
                raise SanicException("Date cannot be in the past.", status_code=403)

        return json(item.to_dict())


class SingleItemView(HTTPMethodView):
    async def get(self, request, id):
        async_session = await get_async_session()

        async with async_session() as session:
            item = await get_item_by_id(session, id)

            if not item:
                raise SanicException("Item does not exist.", status_code=404)

        return json(item.to_dict())

    async def delete(self, request, id):
        async_session = await get_async_session()

        async with async_session() as session:
            item = await get_item_by_id(session, id)

            if not item:
                raise SanicException("Item does not exist.", status_code=404)

            await delete_item(session, id)
        return json({}, status=201)


item_blueprint = Blueprint("item")
item_blueprint.add_route(ItemView.as_view(), "/item")
item_blueprint.add_route(SingleItemView.as_view(), "/item/<id:int>")
