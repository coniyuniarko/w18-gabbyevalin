from flask import Blueprint, jsonify, request
from w18_gabbyevalin.middlewares.token import token_request, token_required

from w18_gabbyevalin.repositories.user import user_by_email, user_by_id, user_change_password, user_create, user_delete, user_list, user_update


blueprint_user = Blueprint("user", __name__, url_prefix="/user")


@blueprint_user.route("/", methods=["GET"])
@token_required
def list():
    return jsonify([user.to_json() for user in user_list()])


@blueprint_user.route("/<int:id>", methods=["GET"])
@token_required
def by_id(id: int):
    user = user_by_id(id)
    if user is None:
        return jsonify({'error': 'Pengguna tidak ditemukan.'}), 404

    return jsonify(user.to_json()), 200


@blueprint_user.route("/", methods=["POST"])
def create():
    data = request.json
    user = user_by_email(data.get('email'))
    if user:
        return jsonify({'error': 'Email sudah digunakan.'}), 409
    
    user = user_create(
        email=data.get('email'),
        name=data.get('name'),
        password=data.get('password')
    )
    if user is None:
        return jsonify({'error': 'Inputan invalid.'}), 400
    return jsonify(user.to_json()), 200


@blueprint_user.route("/<int:id>", methods=["PUT"])
@token_required
def update(id: int):
    user = user_by_id(id)
    if user is None:
        return jsonify({'error': 'Pengguna tidak ditemukan.'}), 404

    data = request.json
    user_updated = user_update(
        user=user, name=data.get('name'))
    if user_updated is None:
        return jsonify({'error': 'Inputan invalid.'}), 400
    return jsonify(user_updated.to_json()), 200


@blueprint_user.route("/<int:id>", methods=["PATCH"])
@token_required
def update_password(id: int):
    user = user_by_id(id)
    if user is None:
        return jsonify({'error': 'Pengguna tidak ditemukan.'}), 404

    data = request.json
    user_updated = user_change_password(
        user=user, password=data.get('password'))
    if user_updated is None:
        return jsonify({'error': 'Inputan invalid.'}), 400
    return jsonify(user_updated.to_json()), 200


@blueprint_user.route("/<int:id>", methods=["DELETE"])
@token_required
def delete(id: int):
    user = user_by_id(id)
    if user is None:
        return jsonify({'error': 'Pengguna tidak ditemukan.'}), 404
    
    token = token_request()
    if token["user"]["id"] == user.id:
        return jsonify({'error': 'Tidak diperkenankan untuk menghapus diri sendiri.'}), 400

    if user_delete(user):
        return '', 200

    return jsonify({'error': 'Inputan invalid.'}), 400
