from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app.api.models import Order
orders_blueprint = Blueprint("orders", __name__)
api = Api(orders_blueprint)

class OrderView(Resource):
    def post(self):
        post_data = request.get_json()
        inventory_id = post_data.get("inventory_id")
        quantity = post_data.get("quantity")
        customer_id = post_data.get("customer_id")
        response_object = {}
        order = Order(inventory_id=inventory_id, quantity=quantity, customer_id=customer_id, status_id=1)
        order.save()
        response_object = {
            "message": "success",
            "order": order.json()
        }
        return response_object, 201
    def get(self):
        orders = Order.query.all()
        return {"orders": [order.json() for order in orders]}, 200
        
api.add_resource(OrderView, "/orders")