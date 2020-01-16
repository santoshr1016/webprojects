from flask import Flask

from url_shortner.extensions import db
from url_shortner.routes import short


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)

    app.register_blueprint(short)
    return app
