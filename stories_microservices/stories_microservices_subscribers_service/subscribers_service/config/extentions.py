import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from subscribers_service.app import app
from flask_marshmallow import Marshmallow
from flasgger import Swagger

settings = {
    'prod': 'subscribers_service.config.production.ProdConfig',
    'dev': 'subscribers_service.config.development.DevConfig',
}


def get_config():
    if PROD:
        return settings.get('prod')
    return settings.get('dev')

DEBUG = False if os.environ.get('DEBUG') else True
PROD = not DEBUG


app.config.from_object(get_config())


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://db_user:bTmNECmEZOrdUcX4DQkAGevLtRakY@127.0.0.1:5434/db_name'
# app.config['SECRET_KEY'] = 'this is private'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config["CELERY_BROKER_URL"] = "redis://:12345@localhost:6379/0"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
swagger = Swagger(app)
