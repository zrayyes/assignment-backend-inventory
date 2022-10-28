def test_get_all_items_for_storage(app):
    _, response = app.test_client.get("/storage/space/1")

    assert response.status == 200
    assert response.json["items"] == []
