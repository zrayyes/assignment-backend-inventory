import pytest


@pytest.mark.asyncio
async def test_create_new_item_type(app):
    pass


# parameterize
@pytest.mark.asyncio
async def test_create_new_item_type_invalid(app):
    pass


@pytest.mark.asyncio
async def test_create_item_type_duplicate_name(app):
    pass


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
