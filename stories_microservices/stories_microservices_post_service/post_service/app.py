from flask import Flask

app = Flask(__name__)

from .config.extentions import db
from .models import *
from .api.routers import api
from .subscriber import subscribe


# app.config["APPLICATION_ROOT"] = "api/v1.0/post/"

app.register_blueprint(api, url_prefix='/api/v1.0/posts')

@app.before_first_request
def _run_on_start():
    subscribe()


if __name__ == '__main__':
    # app.init_app(db)
    app.run(port=5001, debug=True)
