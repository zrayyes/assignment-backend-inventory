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

    # TODO: Also return storage space info
    assert response.status == 200
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["type"] == "crackers"


@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_sorted(
    add_storage_space, add_item_type, add_item, app
):
    pass


# Add parameterize
@pytest.mark.asyncio
async def test_get_all_items_for_storage_space_invalid():
    pass


@pytest.mark.asyncio
async def test_create_new_storage_space_valid():
    pass


# Add parameterize
@pytest.mark.asyncio
async def test_create_new_storage_space_invalid():
    pass


@pytest.mark.asyncio
async def test_rename_storage_space():
    pass


@pytest.mark.asyncio
async def test_delete_storage_space_empty():
    pass


@pytest.mark.asyncio
async def test_delete_storage_space_not_empty():
    pass
