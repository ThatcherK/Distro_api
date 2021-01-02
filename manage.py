from flask.cli import FlaskGroup
from sqlalchemy import text

from app import create_app, db
from app.api.models import Role, Status, User,InvitedUser

app = create_app()
cli = FlaskGroup(create_app=create_app)

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

@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    create_status()
    create_roles()
    db.session.add(InvitedUser('owner@distro.com', 'owner', 1))
    db.session.commit()

if __name__ == "__main__":
    cli()