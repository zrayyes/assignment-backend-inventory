import pytest


@pytest.mark.asyncio
async def test_create_new_item_type(app):
    body = {"name": "Milk", "needs_fridge": True}
    url = app.url_for("item_type.ItemTypeView")
    _, response = await app.asgi_client.post(url, json=body)

    assert response.status == 200
    assert response.json["name"] == body["name"]
    assert response.json["needs_fridge"] == body["needs_fridge"]
    assert "id" in response.json


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_body",
    [
        {"name": "Milk"},
        {"needs_fridge": True},
    ],
)
async def test_create_new_item_type_invalid(app, request_body):
    url = app.url_for("item_type.ItemTypeView")
    _, response = await app.asgi_client.post(url, json=request_body)

    assert response.status == 400


@pytest.mark.asyncio
async def test_create_item_type_duplicate_name(add_item_type, app):
    # Create item type
    await add_item_type("Milk", True)

    # Send a request to create an item type with the same name
    body = {"name": "Milk", "needs_fridge": True}
    url = app.url_for("item_type.ItemTypeView")
    _, response = await app.asgi_client.post(url, json=body)

    assert response.status == 403


@pytest.mark.asyncio
async def test_get_existing_item_type(app, add_item_type):
    item_type = await add_item_type("Milk", True)

    url = app.url_for("item_type.SingleItemTypeView", id=item_type.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert response.json["name"] == "Milk"
    assert response.json["needs_fridge"] is True


@pytest.mark.asyncio
async def test_get_non_existing_item_type(app):
    url = app.url_for("item_type.SingleItemTypeView", id=1)
    _, response = await app.asgi_client.get(url)

    assert response.status == 404


@pytest.mark.asyncio
async def test_rename_existing_item_type(app, add_item_type):
    item_type = await add_item_type("Milk", True)

    body = {"name": "Old Milk"}
    url = app.url_for("item_type.SingleItemTypeView", id=item_type.id)
    _, response = await app.asgi_client.patch(url, json=body)

    assert response.status == 200
    assert response.json["id"] == item_type.id
    assert response.json["name"] == body["name"]
    assert response.json["needs_fridge"] == item_type.needs_fridge


@pytest.mark.asyncio
async def test_rename_existing_item_type_to_duplicate(add_item_type, app):
    item_type = await add_item_type("Milk", True)
    other_item_type = await add_item_type("Old Milk", True)

    body = {"name": "Old Milk"}
    url = app.url_for("item_type.SingleItemTypeView", id=item_type.id)
    _, response = await app.asgi_client.patch(url, json=body)

    assert response.status == 403
    assert (
        response.json["message"]
        == f"Item type with same name already exists. ItemType = {other_item_type.id}"
    )


@pytest.mark.asyncio
async def test_delete_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_delete_non_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_delete_item_type_with_items(app):
    pass
