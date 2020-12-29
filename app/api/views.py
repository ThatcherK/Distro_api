from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app import bcrypt, db
from app.api.models import User

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

class RegisterUser(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        role_id = post_data.get("role_id")
        business_id = post_data.get("business_id")
        

