import pytest

from src.helpers import date_after_n_days


@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_sorted(
    add_storage_space, add_item_type, add_item, app
):
    space = await add_storage_space("small space", 5, False)

    # Setup items
    days = [3, 1, 500, 250]
    items = []

    for day in days:
        item_type = await add_item_type(name=f"day {day}")
        item = await add_item(space, item_type, date_after_n_days(day))
        items.append(item)

    # Test for ascending sort
    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id, sort="ASC")
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert len(response.json["items"]) == 4

    days.sort()
    for index, item in enumerate(response.json["items"]):
        assert item["type"] == f"day {days[index]}"

    # Test for descending sort
    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id, sort="DESC")
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert len(response.json["items"]) == 4

    days.sort()
    days.reverse()
    for index, item in enumerate(response.json["items"]):
        assert item["type"] == f"day {days[index]}"


@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_sorted_and_paginated(
    add_storage_space, add_item_type, add_item, app
):
    space = await add_storage_space("small space", 5, False)

    # Setup items
    days = [3, 1, 500, 250]
    items = []

    for day in days:
        item_type = await add_item_type(name=f"day {day}")
        item = await add_item(space, item_type, date_after_n_days(day))
        items.append(item)

    # Fetch first page
    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id, count=2)
    _, response = await app.asgi_client.get(url)

    # Validate first page
    assert response.status == 200
    assert len(response.json["items"]) == 2
    assert response.json["items"][0]["type"] == f"day {days[0]}"
    assert response.json["items"][1]["type"] == f"day {days[1]}"

    # Fetch second page
    url = app.url_for(
        "storage_space.SingleStorageSpaceView", id=space.id, count=2, offset=2
    )
    _, response = await app.asgi_client.get(url)

    # Validate second page
    assert response.status == 200
    assert len(response.json["items"]) == 2
    assert response.json["items"][0]["type"] == f"day {days[2]}"
    assert response.json["items"][1]["type"] == f"day {days[3]}"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params",
    [
        {"sort": "Big", "count": 0, "offset": 0},
        {"sort": "ASC", "count": -1, "offset": 0},
        {"sort": "DESC", "count": 0, "offset": -1},
    ],
)
async def test_get_all_items_for_storage_space_invalid(app, add_storage_space, params):
    space = await add_storage_space("small space", 5, False)

    url = app.url_for(
        "storage_space.SingleStorageSpaceView",
        id=space.id,
        sort=params["sort"],
        count=params["count"],
        offset=params["offset"],
    )
    _, response = await app.asgi_client.get(url)

    assert response.status == 403


@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_does_not_exist(app):
    url = app.url_for("storage_space.SingleStorageSpaceView", id=1)
    _, response = await app.asgi_client.get(url)

    assert response.status == 404


@pytest.mark.asyncio
async def test_create_new_storage_space_valid(app):
    body = {"name": "Big", "capacity": 100, "is_refrigerated": True}
    url = app.url_for("storage_space.StorageSpaceView")
    _, response = await app.asgi_client.post(url, json=body)

    assert response.status == 200
    assert response.json["name"] == body["name"]
    assert response.json["capacity"] == body["capacity"]
    assert response.json["is_refrigerated"] == body["is_refrigerated"]
    assert "id" in response.json


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body",
    [
        {"name": "Big", "is_refrigerated": True},
        {
            "name": "Big",
            "capacity": 100,
        },
        {"capacity": 100, "is_refrigerated": True},
        {"name": "Big", "capacity": -1, "is_refrigerated": True},
    ],
)
async def test_create_new_storage_space_invalid(app, request_body):
    url = app.url_for("storage_space.StorageSpaceView")
    _, response = await app.asgi_client.post(url, json=request_body)

    assert response.status == 400


@pytest.mark.asyncio
async def test_rename_storage_space(add_storage_space, app):
    space = await add_storage_space("small space", 5, False)

    body = {"name": "bigger space"}
    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.patch(url, json=body)

    assert response.status == 200
    assert response.json["name"] == body["name"]
    assert response.json["capacity"] == space.capacity
    assert response.json["is_refrigerated"] == space.is_refrigerated
    assert response.json["id"] == space.id


@pytest.mark.asyncio
async def test_delete_storage_space_empty(add_storage_space, app):
    space = await add_storage_space("small space", 5, False)

    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.delete(url)

    assert response.status == 201

    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 404


@pytest.mark.asyncio
async def test_delete_storage_space_not_empty(
    add_storage_space, add_item_type, add_item, app
):
    space = await add_storage_space("small space", 5, False)
    item_type = await add_item_type("crackers", False)
    await add_item(space, item_type)

    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.delete(url)

    assert response.status == 403
    assert response.json["message"] == "Storage space still has items attached."

    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert len(response.json["items"]) > 0
