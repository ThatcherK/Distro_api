import datetime
import os
import jwt
import json
from flask import current_app

from app import bcrypt, db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=True)

    def __init__(self, username, password, role_id, business_id=None):
        self.username= username
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()
        self.role_id = role_id
        self.business_id = business_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        role = Role.query.filter_by(id=self.role_id).first()
        business = Business.query.filter_by(id=self.business_id).first()
        data = {}
        if business:
            data = {
                "id": self.id,
                "username": self.username,
                "password": self.password,
                "role": role.json(),
                "business": business.name,
            }
        else:
            data = {
                "id": self.id,
                "username": self.username,
                "password": self.password,
                "role": role.json(),
                "business": "",
            }
        return data

    def encode_auth_token(self, user_id):
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    days=current_app.config.get("TOKEN_EXPIRATION_DAYS"),
                    seconds=current_app.config.get("TOKEN_EXPIRATION_SECONDS"),
                ),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(
                payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return e.__str__()

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"),algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Expired token. Please Log in again"
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again"

    def __repr__(self):
        return f"<User, {self.username, self.password, self.role_id, self.business_id}>"

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)

    def __init__(self, name, quantity, price, business_id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.business_id = business_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        business = Business.query.filter_by(id=self.business_id).first()
        data = {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "business": business.name,
        }
        return data

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    delivery_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, inventory_id, quantity, status_id, customer_id, transporter_id=None, delivery_date=None):
        self.inventory_id = inventory_id
        self.quantity= quantity
        self.transporter_id = transporter_id
        self.status_id = status_id
        self.customer_id = customer_id
        self.delivery_date = delivery_date

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        item = Inventory.query.filter_by(id=self.inventory_id).first()
        transporter = User.query.filter_by(id=self.transporter_id).first()
        customer = Customer.query.filter_by(id=self.customer_id).first()
        status = Status.query.filter_by(id = self.status_id).first()
        data = {}
        if transporter:
            data = {
                "id": self.id,
                "name": item.name,
                "quantity": self.quantity,
                "transporter": transporter.username,
                "customer": customer.username,
                "order_date": self.order_date.strftime("%d %b %Y "),
                "delivery_date": self.delivery_date.strftime("%d %b %Y ") if self.delivery_date else None,
                "status": status.name
            }
        else:
            data = {
                "id": self.id,
                "name": item.name,
                "quantity": self.quantity,
                "customer": customer.username,
                "order_date": self.order_date.strftime("%d %b %Y "),
                "delivery_date": self.delivery_date.strftime("%d %b %Y") if self.delivery_date else None,
                "status": status.name
            }
        return data

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        data = {"id": self.id, "name": self.name}
        return data

class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    business_owner_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, business_owner_id):
        self.name = name
        self.business_owner_id = business_owner_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        business_owner = User.query.filter_by(id=self.business_owner_id).first()
        data = {
            "id": self.id, 
            "name": self.name,
            "business_owner": business_owner.json()
            }
        return data

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        data = {"id": self.id, "name": self.name}
        return data

class InvitedUser(db.Model):
    __tablename__ = 'invited_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    invite_code = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    def __init__(self, email, invite_code, role_id):
        self.email = email
        self.invite_code = invite_code
        self.role_id = role_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        role = Role.query.filter_by(id=self.role_id).first()
        data = {
            "id": self.id,
            "email": self.email,
            "invite_code": self.invite_code,
            "role": role.name,
        }
        return data
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    orders = db.relationship("Order", backref='customer', lazy=True)

    def __init__(self, username, password, phone_number, role_id):
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()
        self.phone_number = phone_number
        self.role_id = role_id

    def encode_auth_token(self, user_id):
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    days=current_app.config.get("TOKEN_EXPIRATION_DAYS"),
                    seconds=current_app.config.get("TOKEN_EXPIRATION_SECONDS"),
                ),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(
                payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
            )
        except Exception as e:
            return e.__str__()

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Expired token. Please Log in again"
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        role = Role.query.filter_by(id=self.role_id).first()
        data = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "phone_number": self.phone_number,
            "role": role.name,
        }
        return data

