import json

def test_add_business(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp = client.post(
        "/business",
        data=json.dumps({"name": "distro"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 201
    assert "distro" in data["business"].get("name")

def test_add_business_no_authtoken(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/business",
        data=json.dumps({"name": "distro"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 401

# def test_get_business(test_app):
    # client = test_app.test_client()
    # resp = client.get("/business")
    # data = json.loads(resp.data.decode())

    # assert resp.status_code == 200
