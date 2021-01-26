from ..app import app
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from flask_mongoengine import MongoEngine

db = MongoEngine(app)
ma = Marshmallow(app)
swagger = Swagger(app)
