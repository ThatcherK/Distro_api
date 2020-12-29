import datetime
import os
import jwt

from app import bcrypt, db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)

    def __init__(self, username, password, role_id, business_id):
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
        data = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": role.name,
            "business": business.name,
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
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"))
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
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"), nullable=False)

    def __init__(self, name, business_id):
        self.name= name
        self.business_id = business_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        business = Business.query.filter_by(id=self.business_id).first()
        data = {
            "id": self.id,
            "name": self.name,
            "business": business.name,
        }
        return data

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    transporter_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"),nullable=True)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    delivery_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, inventory_id, quantity, transporter_id, status_id, order_date, delivery_date):
        self.inventory_id = inventory_id
        self.quantity= quantity
        self.transporter_id = transporter_id
        self.status_id = status_id
        self.order_date = order_date
        self.delivery_date = delivery_date

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        item = Inventory.query.filter_by(id=self.inventory_id).first()
        business = Business.query.filter_by(id=self.business_id).first()
        transporter = User.query.filter_by(id=self.transporter_id).first()
        data = {
            "id": self.id,
            "name": item.name,
            "quantity": self.quantity,
            "transporter": transporter.username
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

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        data = {"id": self.id, "name": self.name}
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

# class Customer(db.Model):
#     pass