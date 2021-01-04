import json

from app import db
from app.api.models import Business, Inventory, Customer

def test_add_order(test_app, test_database):
    client = test_app.test_client()
    db.session.add(Business("distro",1))
    db.session.commit()
    db.session.add(Inventory("paper", 100, 100, 1))
    db.session.add(Customer("Mary", "password", "0707625384", 5))
    db.session.commit()
    resp = client.post(
        "/orders",
        data=json.dumps(
            {
                "inventory_id": 1,
                "quantity": 2,
                "customer_id": 1,   
            }
        ),
        content_type="application/json",
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "success" in data.get("message")

def test_add_order_higher_quantity_than_stock(test_app, test_database):
    client = test_app.test_client()
    db.session.add(Business("distro",1))
    db.session.commit()
    db.session.add(Inventory("paper", 100, 100, 1))
    db.session.add(Customer("Mary", "password","0759738261", 5))
    db.session.commit()
    resp = client.post(
        "/orders",
        data=json.dumps(
            {
                "inventory_id": 1,
                "quantity": 101,
                "customer_id": 1,   
            }
        ),
        content_type="application/json",
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Required quantity exceeds the stock" in data.get("message")