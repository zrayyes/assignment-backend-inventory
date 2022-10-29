import pytest


@pytest.mark.asyncio
async def test_get_all_items_for_storage(
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
