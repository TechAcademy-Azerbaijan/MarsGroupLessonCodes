from flask import Flask


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://db_user:12345@127.0.0.1:27017/db_name?authSource=admin',
    'connect': True
}

from .config.extentions import *
from .models import *
from .api.routers import *

# app.config["APPLICATION_ROOT"] = "api/v1.0/post/"

if __name__ == '__main__':
    # app.init_app(db)
    app.run(port=5001, debug=True)

