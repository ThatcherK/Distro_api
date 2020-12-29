from uuid import uuid4

from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app import bcrypt, db
from app.api.models import User, InvitedUser
from app.api.utils import send_invite_email

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

class InviteUser(Resource):
    def post(self):
        post_data = request.get_json()
        print(post_data)
        email = post_data.get("email")
        role_id = post_data.get("role_id")
        if (email  and role_id) == "":
            response_object = {"message": "Invalid payload"}
            return response_object, 400
        invite_code = str(uuid4())
        invited_user = InvitedUser(email, invite_code, role_id)
        invited_user.save()
        if current_app.config != "testing":
            send_invite_email(invite_code, invited_user.email, "http://localhost:3000/")
        return {"invitedUser": invited_user.json()}, 200

    def get(self):
        invited_users = InvitedUser.query.all()
        return {"invited_users": [user.json() for user in invited_users]}, 200   

api.add_resource(InviteUser, "/invited_users")
