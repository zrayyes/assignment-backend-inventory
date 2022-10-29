import pytest


@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_valid(
    add_storage_space, add_item_type, add_item, app
):
    space = await add_storage_space("small space", 5, False)
    item_type = await add_item_type("crackers", False)
    await add_item(space, item_type)

    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["type"] == "crackers"
    assert response.json["name"] == "small space"
    assert response.json["capacity"] == 5
    assert response.json["is_refrigerated"] is False


@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_sorted(
    add_storage_space, add_item_type, add_item, app
):
    pass


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
async def test_delete_storage_space_empty(app):
    pass


@pytest.mark.asyncio
async def test_delete_storage_space_not_empty(app):
    pass
