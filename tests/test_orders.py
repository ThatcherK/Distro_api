import json

from app import db
from app.api.models import Business, Inventory, Customer

def test_add_order(test_app):
    client = test_app.test_client()
    db.session.add(Business("distro"))
    db.session.commit()
    db.session.add(Inventory("paper", 100, 1))
    db.session.add(Customer("Mary", "password", 5))
    db.session.commit()
    resp = client.post(
        "/oders",
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
    # assert "Success" in data.get("status")
