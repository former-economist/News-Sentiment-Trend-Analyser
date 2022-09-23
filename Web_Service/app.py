import os

import sqlalchemy
from flask import Flask
from flask_cors import CORS

from models import database


def db_uri():
    """
    Generate database URI

    Returns:
        str: URI connection string.
    """
    db_str = "mariadb+mariadbconnector"
    uri = db_str + "://"
    uri += os.environ.get("DB_USER", default="none") + ":"
    uri += os.environ.get("DB_PASSWORD", default="none") + "@"
    uri += os.environ.get("DB_SERVER", default="127.0.0.1") + ":"
    uri += os.environ.get("DB_PORT", default="3306") + "/"
    uri += os.environ.get("DB_NAME", default="mydb")
    return uri


def create_app(test_config: dict = {}):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '$SECRET_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if len(test_config) > 0:
        app.config.update(test_config)
    with app.app_context():
        database.init_app(app)
        database.create_all()
    CORS(app)
    from routes import authorise_bp, home_bp, saved_bp, search_bp
    app.register_blueprint(search_bp)
    app.register_blueprint(authorise_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(saved_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    svc_host = os.environ.get("SVC_HOST", default=None)
    print(svc_host)
    app.run(debug=True, host=svc_host)
