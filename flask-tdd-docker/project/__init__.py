"""
Yes, our app is being created in application/__init__.py, so a file called wsgi.py
simply imports this file to serve as our app gateway

Derive our app's config from a class, file, or environment variables.
Initialize plugins accessible to any part of our app, such as a database or login logic with Flask-Login.
Set any variables we want to be accessible globally.
Import the logic which makes u our app (such as routes).
Register Blueprints.

The init file is where we actually create what's called the
Application Factory.
"""

import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

""" Step 1: Creating Instances of Plugin Objects
instantiate db, FlaskRedis, FlaskLogin etc
 """
db = SQLAlchemy()


def create_app(script_info=None):
    """ Step 2: App Creation
    we're creating our Flask app object and stating that it should be configured using a
    class called Config in a file named config.py:
    """
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    """ Step 3: Plugin Initialization
    After the app object is created, we then "initialize" those plugins we mentioned earlier. 
    Initializing a plugin registers a plugin with our Flask app.
    """
    db.init_app(app)

    """  Step 4: The Application Context
    This block is the lifeblood of our Flask app 
    it's essentially saying "here are all the pieces of my program."
    """
    # Register the Blueprints
    from project.api.ping import ping_blueprint
    from project.api.users import users_blueprint
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)


    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
