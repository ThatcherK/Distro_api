from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app.api.models import Inventory

inventory_blueprint = Blueprint("inventory", __name__)
api = Api(inventory_blueprint)

class InventoryView(Resource):
    def post(self):
        post_data = request.get_json()
        name = post_data.get("name")
        quantity = post_data.get("quantity")
        business_id = 1
        new_item = Inventory(name, quantity, business_id)
        new_item.save()
        response_object = {
            "message": "success",
            "item": new_item.json()
        }
        return response_object,201

    def get(self):
        inventory = Inventory.query.all()
        return {"inventory": [item.json() for item in inventory]}, 200  

    
api.add_resource(InventoryView, "/inventory")

class InventoryDetailView(Resource):
    def patch(self,id):
        post_data = request.get_json()
        name = post_data.get("name")
        quantity = post_data.get("quantity")
        item = Inventory.query.filter_by(id=id).first()
        if item:
            item.name = name
            item.quantity = quantity
            item.save()
            response_object = {
                "message": "success",
                "item": item.json()
            }
            return response_object,200

    def get(self,id):
        item = Inventory.query.filter_by(id=id).first()
        response_object = {}
        if item:
            response_object = {
                "item": item.json()
            }
            return response_object, 200
        else:
            response_object = {
                "message": "This item does not exist"
            }
            return response_object, 404

api.add_resource(InventoryDetailView, "/inventory/<int:id>")