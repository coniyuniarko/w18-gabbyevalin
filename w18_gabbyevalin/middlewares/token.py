from datetime import timedelta
from functools import wraps
import time

from flask import current_app, request
import jwt

from w18_gabbyevalin.repositories.user import user_by_email


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = token_request()
        if not token:
            return {'error': 'Token invalid.'}, 401

        if token["expired"]:
            return {'error': 'Token kadaluwarsa.'}, 401

        return func(*args, **kwargs)

    return decorated


def token_generate(email: str) -> str:
    data = {
        "email": email,
        "expired": time.time() + timedelta(days=180).total_seconds()
    }
    return jwt.encode(data, current_app.config["SECRET_KEY"], algorithm="HS256")


def token_request() -> dict:
    token = request.cookies.get('Authorization')
    if token is None and "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    if not token:
        return None
    try:
        data = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

        if data["expired"] < time.time():
            return None

        user = user_by_email(data["email"])
        return {
            "expired": data["expired"] < time.time(),
            "user": user.to_json()
        }
    except Exception as e:
        return None
