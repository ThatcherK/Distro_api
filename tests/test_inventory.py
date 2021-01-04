import json
from app import db
from app.api.models import Business, Inventory
def test_add_inventory(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    db.session.add(Business("distro", 1))
    db.session.commit()
    resp = client.post(
        "/inventory",
        data=json.dumps(
            {
                "name": "boats",
                "quantity": 10,
                "price": 1000000,
                "business_id": 1,
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "success" in data.get("message")
  
def test_add_inventory_invalid_json(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    db.session.add(Business("distro", 1))
    db.session.commit()
    resp = client.post(
        "/inventory",
        data=json.dumps(
            {
              
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload" in data.get("message")

def test_add_inventory_missing_fields(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    db.session.add(Business("distro", 1))
    db.session.commit()
    resp = client.post(
        "/inventory",
        data=json.dumps(
            {
              "name": "boats",
              "quantity": 10,
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload" in data.get("message")

def test_get_inventory(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    db.session.add(Business("distro", 1))
    db.session.commit()
    db.session.add(Inventory("paper", 1000, 1000, 1))
    db.session.commit()
    resp = client.get("/inventory")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data.get("inventory")) == 1

def test_update_inventory_detail(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    db.session.add(Business("distro", 1))
    db.session.commit()
    db.session.add(Inventory("paper", 1000, 1000, 1))
    db.session.commit()
    resp = client.patch(
        "/inventory/1",
        data=json.dumps(
            {
              "name": "paper",
              "quantity": 900,
              "price": 500,
              "business_id": 1
            }
        ),
        content_type="application/json",
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert data["item"].get("quantity") == 900

# def test_update_inventory_detail_inexistent_item(test_app):
#     client = test_app.test_client()
#     db.session.add(Business("distro"))
#     db.session.commit()
#     db.session.add(Inventory("paper", 1000, 1))
#     db.session.commit()
#     resp = client.patch(
#         "/inventory/2",
#         data=json.dumps(
#             {
#               "name": "paper",
#               "quantity": 900,
#               "business_id": 1
#             }
#         ),
#         content_type="application/json",
#         )
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 400
#     assert "This item does not exist" in data.get("message")

# def test_get_single_inventory_item(test_app):
#     client = test_app.test_client()
#     db.session.add(Business("dummy"))
#     db.session.commit()
#     db.session.add(Inventory("paper", 1000, 1))
#     db.session.commit()
#     resp = client.get("/inventory/1")
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 200
#     assert "paper" in data["item"].get("name")