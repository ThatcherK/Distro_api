from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app.api.models import Customer

customers_blueprint = Blueprint("customers", __name__)
api = Api(customers_blueprint)

class RegisterCustomer(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        phone_number = post_data.get("phone_number")
        response_object = {}
        new_customer = Customer.query.filter_by(username=username).first()
        if not new_customer:
            customer = Customer(username, password, phone_number, 5)
            customer.save()
            auth_token = customer.encode_auth_token(customer.id)
            response_object = {
                "message": f"{username} was added!",
                "token": auth_token,
                "user": customer.json()
            }
            return response_object,201
        else:
            response_object["message"] = "Username already exists"
            return response_object, 400

    def get(self):
        registered_customers = Customer.query.all()
        return {"registered_customers": [customer.json() for customer in registered_customers]}, 200   

api.add_resource(RegisterCustomer, "/customer/register")

class LoginCustomer(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        try:
            user = Customer.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        "status": "Success",
                        "token": auth_token.decode(),
                        "user": user.json(),
                    }
                return response_object, 200
            response_object = {
                "status": "Fail",
                "message": "Invalid username or password",
                "token": None,
            }
            return response_object, 401
        except Exception:
            response_object = {
                "status": "Fail",
                "message": "Invalid credentials",
                "token": None,
            }
            return response_object, 400

api.add_resource(LoginCustomer, "/customer/login")