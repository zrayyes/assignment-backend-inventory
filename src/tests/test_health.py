def test_health_check(app):
    _, response = app.test_client.get("/health_check")

    assert response.status == 200
    assert response.json["status"] == "success"
