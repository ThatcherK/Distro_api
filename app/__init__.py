import os
from flask import Flask,current_app
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(script_info=None):
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    CORS(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    from app.api.views.users import users_blueprint
    from app.api.views.business import business_blueprint
    from app.api.views.inventory import inventory_blueprint
    from app.api.views.orders import orders_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(business_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(orders_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
