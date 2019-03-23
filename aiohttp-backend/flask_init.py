import os

from flask import Flask
from flask_cors import CORS

from werkzeug.security import generate_password_hash

from mongoengine import *
from .models import *

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='grow'
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    connect(app.config.get('DATABASE'))

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    # Create admin user if it does not exist
    admin = Users.objects(username='admin').first()
    if not admin:
        admin = Users(
                username='admin',
                password=generate_password_hash('admin'),
                email='admin@admin.com'
                )
        admin.save()

    return app
