from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.views import HTTPMethodView

from src.controllers.item import get_item_by_id, delete_item
from src.db import get_async_session


class ItemView(HTTPMethodView):
    async def post(self, request):
        ...


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
