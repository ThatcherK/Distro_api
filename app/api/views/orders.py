from flask import Blueprint, current_app, request
from flask_restx import Api, Resource

orders_blueprint = Blueprint("orders", __name__)
api = Api(orders_blueprint)