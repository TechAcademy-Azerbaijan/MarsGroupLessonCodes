from flask import Flask


app = Flask(__name__)

from subscribers_service.config.extentions import db
from subscribers_service.models import *
from subscribers_service.api.routers import *

# app.config["APPLICATION_ROOT"] = "api/v1.0/post/"


