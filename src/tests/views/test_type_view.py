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
async def test_get_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_get_non_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_rename_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_rename_existing_item_type_to_duplicate(app):
    pass


@pytest.mark.asyncio
async def test_delete_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_delete_non_existing_item_type(app):
    pass


@pytest.mark.asyncio
async def test_delete_item_type_with_items(app):
    pass
