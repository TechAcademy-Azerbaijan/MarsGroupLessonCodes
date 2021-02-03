import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from post_service.app import app
from flask_marshmallow import Marshmallow
from flasgger import Swagger

settings = {
    'prod': 'post_service.config.production.ProdConfig',
    'dev': 'post_service.config.development.DevConfig',
}


def get_config():
    if PROD:
        return settings.get('prod')
    return settings.get('dev')


DEBUG = False if os.environ.get('DEBUG') else True
PROD = not DEBUG

app.config.from_object(get_config())

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
swagger = Swagger(app)
