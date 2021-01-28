from flask import request, jsonify, send_from_directory
from flasgger import swag_from
from http import HTTPStatus
from subscribers_service.app import app
from ..config.extentions import db
from marshmallow.exceptions import ValidationError
from sqlalchemy.sql import text


@app.route('/')
def welcome():
    return 'Welcome'
