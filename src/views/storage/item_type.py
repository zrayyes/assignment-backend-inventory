from dataclasses import dataclass

from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic_ext import validate


@dataclass
class ItemTypeIn:
    name: str
    need_fridge: bool


@dataclass
class ItemTypeUpdate:
    name: str


class SingleItemTypeView(HTTPMethodView):
    async def get(self, request, id):
        pass

    @validate(json=ItemTypeUpdate)
    async def patch(self, request, id, body: ItemTypeUpdate):
        pass

    async def delete(self, request, id):
        pass


class ItemTypeView(HTTPMethodView):
    @validate(json=ItemTypeIn)
    async def post(self, request, body: ItemTypeIn):
        pass


item_type_blueprint = Blueprint("item_type")
item_type_blueprint.add_route(ItemTypeView.as_view(), "/item_type")
item_type_blueprint.add_route(SingleItemTypeView.as_view(), "/item_type/<id:int>")
