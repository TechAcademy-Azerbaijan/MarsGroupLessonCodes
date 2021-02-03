import os
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from auth_service.app import app
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from flask_login import LoginManager
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

settings = {
    'prod': 'auth_service.config.production.ProdConfig',
    'dev': 'auth_service.config.development.DevConfig',
}


def get_config():
    if PROD:
        return settings.get('prod')
    return settings.get('dev')

DEBUG = False if os.environ.get('DEBUG') else True
PROD = not DEBUG


app.config.from_object(get_config())

jwt = JWTManager(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
swagger = Swagger(app)

