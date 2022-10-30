import datetime

import pytest

from src.helpers import date_after_n_days, format_date_to_str


@pytest.mark.asyncio
async def test_get_existing_item(add_storage_space, add_item_type, add_item, app):
    space = await add_storage_space("small space", 5, False)
    item_type = await add_item_type("crackers", False)
    item = await add_item(space, item_type)

    url = app.url_for("item.SingleItemView", id=item.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert response.json["type"] == item_type.name
    assert response.json["storage_space"] == space.name


@pytest.mark.asyncio
async def test_get_non_existing_item(app):
    url = app.url_for("item.SingleItemView", id=4)
    _, response = await app.asgi_client.get(url)

    assert response.status == 404


@pytest.mark.asyncio
async def test_delete_existing_item(app, add_item, add_storage_space, add_item_type):
    space = await add_storage_space("small space", 5, False)
    item_type = await add_item_type("crackers", False)
    item = await add_item(space, item_type)

    url = app.url_for("item.SingleItemView", id=item.id)
    _, response = await app.asgi_client.delete(url)

    assert response.status == 201

    url = app.url_for("item.SingleItemView", id=item.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 404


@pytest.mark.asyncio
async def test_create_item_valid_storage(app, add_storage_space, add_item_type):
    space = await add_storage_space("small space", 5, False)
    item_type = await add_item_type("crackers", False)
    date_str = format_date_to_str(date_after_n_days(1))

    body = {
        "expiry_date": date_str,
        "storage_space_id": space.id,
        "item_type_id": item_type.id,
    }
    url = app.url_for("item.ItemView")
    _, response = await app.asgi_client.post(url, json=body)

    assert response.status == 200
    assert response.json["type"] == item_type.name
    assert response.json["storage_space"] == space.name
    assert response.json["expiry_date"] == date_str


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "date_str",
    ["01/01/2000", format_date_to_str(datetime.date.today())],
)
async def test_create_item_with_expired_date(
    app, add_storage_space, add_item_type, date_str
):
    space = await add_storage_space("small space", 5, False)
    item_type = await add_item_type("crackers", False)

    body = {
        "expiry_date": date_str,
        "storage_space_id": space.id,
        "item_type_id": item_type.id,
    }
    url = app.url_for("item.ItemView")
    _, response = await app.asgi_client.post(url, json=body)

    assert response.status == 403


@pytest.mark.asyncio
async def test_create_item_storage_full(
    app, add_storage_space, add_item_type, add_item
):
    space = await add_storage_space("very small space", 1, False)
    item_type = await add_item_type("crackers", False)
    await add_item(space, item_type)

    date_str = format_date_to_str(date_after_n_days(1))
    body = {
        "expiry_date": date_str,
        "storage_space_id": space.id,
        "item_type_id": item_type.id,
    }
    url = app.url_for("item.ItemView")
    _, response = await app.asgi_client.post(url, json=body)

    assert response.status == 403

    url = app.url_for("storage_space.SingleStorageSpaceView", id=space.id)
    _, response = await app.asgi_client.get(url)

    assert response.status == 200
    assert len(response.json["items"]) == 1


@pytest.mark.asyncio
async def test_create_item_in_incompatible_storage(app):
    pass


@pytest.mark.asyncio
async def test_create_item_with_non_existing_storage(app):
    pass


@pytest.mark.asyncio
async def test_create_item_with_non_existing_type(app):
    pass


@pytest.mark.asyncio
async def test_move_item_to_valid_storage(
    app, add_item, add_storage_space, add_item_type
):
    pass


@pytest.mark.asyncio
async def test_move_item_to_incompatible_storage(
    app, add_item, add_storage_space, add_item_type
):
    pass


@pytest.mark.asyncio
async def test_move_item_to_full_storage(
    app, add_item, add_storage_space, add_item_type
):
    pass


@pytest.mark.asyncio
async def test_move_item_to_non_existing_storage(
    app, add_item, add_storage_space, add_item_type
):
    pass
