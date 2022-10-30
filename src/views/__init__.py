from sanic import Blueprint

from src.views.storage.item import item_blueprint
from src.views.storage.item_type import item_type_blueprint
from src.views.storage.space import storage_space_blueprint

storage_blueprint = Blueprint.group(
    [storage_space_blueprint, item_type_blueprint, item_blueprint],
    url_prefix="/storage",
)
