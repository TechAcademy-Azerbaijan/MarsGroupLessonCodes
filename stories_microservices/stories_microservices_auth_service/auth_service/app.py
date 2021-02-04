from flask import Flask


app = Flask(__name__)

from auth_service.config.extentions import db
from auth_service.models import *
from .api.routers import api

app.register_blueprint(api, url_prefix='/api/v1.0/auth')

# app.config["APPLICATION_ROOT"] = "api/v1.0/post/"

if __name__ == '__main__':
    # app.init_app(db)
    app.run(port=5001, debug=True)

