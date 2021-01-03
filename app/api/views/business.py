from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

from app.api.models import Business, User
from app.api.utils import requires_admin_access


business_blueprint = Blueprint("businesses", __name__)
api = Api(business_blueprint)

class BusinessView(Resource):
    @requires_admin_access
    def post(self):
        post_data = request.get_json()
        header = request.headers.get("Authorization")
        name = post_data.get("name")
        auth_token = header.split(' ')[1]
        user_id = User.decode_auth_token(auth_token)
        user = User.query.filter_by(id=user_id).first()
        response_object = {}
        if user:
            # if user.role_id == 1:
            business = Business(name)
            business.save()
            response_object = {
                "message": "success",
                "business": business.json()
            }
            return response_object, 201
        response_object = {
            "message": "Unauthorized"
        }
        return response_object, 401


    def get(self):
        businesses = Business.query.all()
        return {"businesses": [business.json() for business in businesses]}, 200


api.add_resource(BusinessView, "/business")
