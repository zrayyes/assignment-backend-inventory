import pytest


@pytest.mark.asyncio
async def test_get_existing_item(app, add_item):
    pass


@pytest.mark.asyncio
async def test_get_non_existing_item(app, add_item):
    pass


@pytest.mark.asyncio
async def test_delete_existing_item(app, add_item):
    pass


@pytest.mark.asyncio
async def test_delete_non_existing_item(app):
    pass


@pytest.mark.asyncio
async def test_create_item_valid_storage(app):
    pass


@pytest.mark.asyncio
async def test_create_item_with_expired_date(app):
    pass


@pytest.mark.asyncio
async def test_create_item_all_storage_full(app):
    pass


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
