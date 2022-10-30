from sanic import Blueprint
from sanic.views import HTTPMethodView


class ItemView(HTTPMethodView):
    async def post(self, request):
        ...


class SingleItemView(HTTPMethodView):
    async def get(self, request):
        ...


item_blueprint = Blueprint("item")
item_blueprint.add_route(ItemView.as_view(), "/item")
item_blueprint.add_route(SingleItemView.as_view(), "/item/<id:int>")
