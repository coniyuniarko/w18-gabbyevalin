from datetime import timedelta
from http import HTTPStatus
import json
from flask import Blueprint, Response, jsonify, request
from w18_gabbyevalin.middlewares.token import token_generate

from w18_gabbyevalin.repositories.user import user_by_email


blueprint_auth = Blueprint("auth", __name__, url_prefix="/auth")

@blueprint_auth.route("/login", methods=["POST"])
def login():
    data = request.json
    user = user_by_email(data.get('email'))
    if user is None:
        return jsonify({'error': 'Pengguna tidak ditemukan.'}), 404
    
    if not user.verify_password(data.get('password')):
        return jsonify({'error': 'Password invalid.'}), 400
    
    token = token_generate(email=user.email)
    response_data = json.dumps({
        "Authorization": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    })
    response = Response(status=HTTPStatus.OK, response=response_data, mimetype="application/json")
    response.set_cookie(key="Authorization", value=token, httponly=True, max_age=timedelta(days=180))
    return response

@blueprint_auth.route("/logout", methods=["GET"])
def logout():
    response = Response(status=HTTPStatus.OK)
    response.delete_cookie(key="Authorization")
    return response