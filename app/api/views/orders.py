from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app.api.models import Order, Inventory
orders_blueprint = Blueprint("orders", __name__)
api = Api(orders_blueprint)

class OrderView(Resource):
    def post(self):
        post_data = request.get_json()
        inventory_id = post_data.get("inventory_id")
        quantity = post_data.get("quantity")
        customer_id = post_data.get("customer_id")
        inventory_item = Inventory.query.filter_by(id=inventory_id).first()
        if inventory_item:
            if inventory_item.quantity > quantity:
                order = Order(inventory_id, quantity, customer_id, 1)
                order.save()
                inventory_item.quantity -= quantity
                inventory_item.save()
                response_object = {
                    "message": "success",
                    "order": order.json()
                }
                return response_object, 201
            else:
                response_object = {
                    "message": "Required quantity exceeds the stock"
                }
                return response_object, 400
        response_object = {
            "message": "Not found"
        }
        return response_object, 404

    def get(self):
        orders = Order.query.all()
        return {"orders": [order.json() for order in orders]}, 200
        
api.add_resource(OrderView, "/orders")

class OrderDetailView(Resource):
    def patch(self, id):
        post_data = request.get_json()
        transporter_id = post_data.get("transporter_id")
        ordered_item = Order.query.filter_by(id=id).first()
        if ordered_item:
            ordered_item.transporter_id = transporter_id
            ordered_item.status_id = 2
            ordered_item.save()
            response_object = {
                "message": "success",
                "order": ordered_item.json()
            }
            return response_object, 200
        response_object = {
            "message": "Not found"
        }
        return response_object, 404
api.add_resource(OrderDetailView, "/orders/<int:id>")