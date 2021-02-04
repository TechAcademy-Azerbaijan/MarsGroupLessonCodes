from flask import request, jsonify, send_from_directory
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from werkzeug.security import check_password_hash
from ..config.base import RedisConfig, ACCESS_EXPIRES, REFRESH_EXPIRES
from ..config.extentions import jwt

from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    get_jti
)

from auth_service.config.base import MEDIA_ROOT

from ..api import api
from auth_service.schemas.schemas import UserSchema, LoginSchema
from auth_service.models import User

from auth_service.utils.common import save_file

from auth_service.utils.tokens import confirm_token

revoked_store = RedisConfig.client()


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    print('entry', entry)
    if entry is None:
        return entry == 'true'
    return True


@api.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(MEDIA_ROOT, filename)


@api.route('/register/', methods=['POST'])
def register():
    try:
        data = request.json or request.form
        image = request.files.get('image')
        serializer = UserSchema()
        user = serializer.load(data)
        if image:
            user.image = save_file(image)
        user.is_active = False
        user.save()
        user.send_confirmation_mail()
        return UserSchema().jsonify(user), HTTPStatus.CREATED
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST


@api.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'}), HTTPStatus.OK
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Account not found'}), HTTPStatus.OK
    print('is active', user.is_active)
    if user.is_active:
        return jsonify({'message': 'Account already confirmed. Please login.'}), HTTPStatus.OK
    else:
        user.is_active = True
        user.save()
        return jsonify({'message': 'You have confirmed your account. Thanks!'}), HTTPStatus.OK


@api.route('/login/', methods=['POST'])
def login():
    try:
        data = request.json or request.form
        serializer = LoginSchema()
        user_data = serializer.load(data)
        user = User.query.filter_by(email=user_data['email']).first()
        if user and check_password_hash(user.password, user_data['password']):
            # if not user.is_active:
            #     return jsonify({'message': 'Please confirm your account'}), HTTPStatus.OK
            user = UserSchema().dump(user)
            access_token = create_access_token(identity=user['id'])
            refresh_token = create_refresh_token(identity=user['id'])
            user.update({
                'access_token': access_token,
                'refresh_token': refresh_token
            })
            return jsonify(user), HTTPStatus.OK
        else:
            return jsonify({'message': 'Bad username or password'}), HTTPStatus.UNAUTHORIZED
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST


@api.route('/user-profile/')
@jwt_required
def user_profile():
    user_id = get_jwt_identity()
    # user = User.query.filter_by(email=user_email, is_active=True).first()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'Not found'}), HTTPStatus.UNAUTHORIZED
    return UserSchema().jsonify(user), HTTPStatus.OK

# Endpoint for revoking the current users access token
@api.route('/access-revoke/', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)
    return jsonify({"msg": "Access token revoked"}), 200


# Endpoint for revoking the current users refresh token
@api.route('/refresh_revoke/', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    revoked_store.set(jti, 'true', REFRESH_EXPIRES * 1.2)
    return jsonify({"msg": "Refresh token revoked"}), 200


@api.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})


@api.route('/refresh-token/', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    user_id = get_jwt_identity()
    print('user_email', user_id)
    ret = {
        'access_token': create_access_token(identity=user_id)
    }
    return jsonify(ret), HTTPStatus.OK
