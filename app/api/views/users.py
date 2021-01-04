from uuid import uuid4

from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app import bcrypt, db
from app.api.models import User, InvitedUser
from app.api.utils import send_invite_email, requires_admin_access, validate_invite_user

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

class InviteUser(Resource):
    @validate_invite_user
    @requires_admin_access
   
    def post(self):
        post_data = request.get_json()
        print(post_data)
        email = post_data.get("email")
        role_id = post_data.get("role_id")
        invite_check_user = InvitedUser.query.filter_by(email=email).first()
        if invite_check_user:
            response_object = {
                "message": "This user was already invited"
            }
            print(response_object)
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

class RegisterUser(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        business_id = post_data.get("business_id")
        invite_code = post_data.get("invite_code")
        response_object = {}
        invited_user = InvitedUser.query.filter_by(invite_code=invite_code).first()
        if invited_user:
            role_id = invited_user.role_id
            user_check = User.query.filter_by(username=username).first()
            if user_check:
                return {"message": "This user already exists"},400
            user = User(username, password, role_id, business_id)
            user.save()
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                "message": f"{username} was added!",
                "token": auth_token,
                "user": user.json()
            }
            return response_object,201
        else:
            response_object["message"] = "Not authorised"
            return response_object, 401

    def get(self):
        registered_users = User.query.all()
        return {"registered_users": [user.json() for user in registered_users]}, 200   

api.add_resource(RegisterUser, "/register")

class Login(Resource):
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        password = post_data.get("password")
        if username == None or password == None:
            return {"message": "Invalid payload"}, 400
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    "status": "Success",
                    "token": auth_token,
                    "user": user.json(),
                }
            return response_object, 200
        response_object = {
            "status": "Fail",
            "message": "Invalid username or password",
            "token": None,
        }
        return response_object, 401
        # except Exception:
        #     response_object = {
        #         "status": "Fail",
        #         "message": "Invalid credentials",
        #         "token": None,
        #     }
        #     return response_object, 400

api.add_resource(Login, "/login")

class StaffView(Resource):
    def get(self):
        all_staff = User.query.filter(User.role_id > 1).all()
        return {"staff": [user.json() for user in all_staff]}, 200

api.add_resource(StaffView, "/staff")

class StaffDetailView(Resource):
    def patch(self, id):
        post_data = request.get_json()
        username = post_data.get("username")
        role_id = post_data.get("role_id")
        staff = User.query.filter_by(id=id).first()
        response_object = {}
        if staff:
            staff.username = username
            staff.role_id = role_id
            staff.save()
            response_object = {
                "message": "success"
            }
            return response_object, 200
        response_object = {
            "message": "User does not exist"
        }
        return response_object, 404

api.add_resource(StaffDetailView, "/staff/<int:id>")