from dataclasses import dataclass
from typing import Optional

from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from src.controllers.storage_space import (create_storage_space,
                                           delete_storage_space,
                                           get_all_items_for_storage_space,
                                           get_storage_space_by_id,
                                           update_storage_space)
from src.db import get_async_session


@dataclass
class StorageSpaceIn:
    name: str
    capacity: int
    is_refrigerated: bool


@dataclass
class StorageSpaceUpdate:
    name: str


@dataclass
class SortPaginateParams:
    sort: Optional[str] = None
    count: Optional[int] = None
    offset: int = 0


class SingleStorageSpaceView(HTTPMethodView):
    @validate(query=SortPaginateParams)
    async def get(self, request, id, query: SortPaginateParams):

        # valdidate sorting
        if query.sort != "None":
            if query.sort not in ["ASC", "DESC"]:
                raise SanicException(
                    "Invalid sort direction. Please use 'ASC' or 'DESC'.",
                    status_code=403,
                )

        # valdidate count
        if query.count:
            if query.count < 0:
                raise SanicException(
                    "Please enter count greater that or equal to 0.",
                    status_code=403,
                )

        # valdidate offset
        if query.offset:
            if query.offset < 0:
                raise SanicException(
                    "Please enter offset greater that or equal to 0.",
                    status_code=403,
                )

        async_session = await get_async_session()

        async with async_session() as session:
            space = await get_storage_space_by_id(session, id)

            if not space:
                raise SanicException("Storage space does not exist.", status_code=404)

            items = await get_all_items_for_storage_space(
                session, space.id, query.sort, query.count, query.offset
            )

            items = [item.to_dict() for item in items]

        output = space.to_dict()
        output["items"] = items
        return json(output)

    @validate(json=StorageSpaceUpdate)
    async def patch(self, request, id, body: StorageSpaceUpdate):
        async_session = await get_async_session()

        async with async_session() as session:
            space = await get_storage_space_by_id(session, id)

            if not space:
                raise SanicException("Storage space does not exist.", status_code=404)

            update = {}
            update["name"] = body.name

            await update_storage_space(session, space, **update)

        return json(space.to_dict())

    async def delete(self, request, id):
        async_session = await get_async_session()

        async with async_session() as session:
            space = await get_storage_space_by_id(session, id)

            if not space:
                raise SanicException("Storage space does not exist.", status_code=404)

            items = await get_all_items_for_storage_space(session, space.id, None, 1)

            if items:
                raise SanicException(
                    "Storage space still has items attached.", status_code=403
                )

            await delete_storage_space(session, space.id)
        return json({}, status=201)


class StorageSpaceView(HTTPMethodView):
    @validate(json=StorageSpaceIn)
    async def post(self, request, body: StorageSpaceIn):
        if body.capacity < 0:
            raise SanicException(
                "Storage space cannot have capacity less than 0.", status_code=400
            )
        async_session = await get_async_session()
        async with async_session() as session:
            space = await create_storage_space(
                session,
                name=body.name,
                capacity=body.capacity,
                is_refrigerated=body.is_refrigerated,
            )
        return json(space.to_dict())


storage_space_blueprint = Blueprint("storage_space")
storage_space_blueprint.add_route(StorageSpaceView.as_view(), "/space")
storage_space_blueprint.add_route(SingleStorageSpaceView.as_view(), "/space/<id:int>")
