from sanic import Blueprint

from src.views.storage.space import storage_space_blueprint

storage_blueprint = Blueprint.group(storage_space_blueprint, url_prefix="/storage")
