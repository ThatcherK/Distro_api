import pytest

from app import create_app, db
from app.api.models import Status, Role, User, Business

def create_status():
    db.session.add(Status(name="ordered"))
    db.session.add(Status(name="transit"))
    db.session.add(Status(name="delivered"))

def create_roles():
    db.session.add(Role(name="business_owner"))
    db.session.add(Role(name="transport_manager"))
    db.session.add(Role(name="driver"))
    db.session.add(Role(name="store_manager"))
    db.session.add(Role(name="customer"))
    db.session.commit()

def create_business():
    db.session.add(Business("distro",1))
    # db.session.commit()

def seed_test_db():
    create_status()
    owner = User('Owner','owner', 1)
    db.session.add(owner)
    create_business()
    db.session.commit()
    token = owner.encode_auth_token(owner.id)
    return token

@pytest.fixture(scope="function")
def test_app():
    app = create_app()
    app.config.from_object("config.TestingConfig")
    with app.app_context():
        yield app

@pytest.fixture(scope="function")
def test_database():
    db.create_all()
    create_roles()
    test_auth_token = seed_test_db()
    yield db, test_auth_token
    db.session.remove()
    db.drop_all()
