from os import environ
from flask import Blueprint, Flask
from flask_cors import CORS
from w18_gabbyevalin.db import db
from w18_gabbyevalin.routes import product, user, auth


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    bp = Blueprint("bp", __name__, url_prefix=environ.get("ROOT_PATH"))

    bp.register_blueprint(product.blueprint_product)
    bp.register_blueprint(user.blueprint_user)
    bp.register_blueprint(auth.blueprint_auth)

    app.register_blueprint(bp)

    return app
