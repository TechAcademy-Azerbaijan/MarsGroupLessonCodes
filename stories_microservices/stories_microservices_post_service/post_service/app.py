from flask import Flask

app = Flask(__name__)

from .config.extentions import db
from .models import *
from .api.routers import *
from .subscriber import subscribe

# app.config["APPLICATION_ROOT"] = "api/v1.0/post/"

subscribe()

if __name__ == '__main__':
    # app.init_app(db)
    app.run(port=5001, debug=True)
