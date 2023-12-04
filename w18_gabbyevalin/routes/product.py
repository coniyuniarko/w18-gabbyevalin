import datetime
from flask import Blueprint, jsonify, request
from w18_gabbyevalin.middlewares.token import token_required
from w18_gabbyevalin.model import Product
from w18_gabbyevalin.repositories.product import product_by_id, product_create, product_delete, product_list, product_update


blueprint_product = Blueprint("product", __name__, url_prefix="/product")


@blueprint_product.route("/", methods=["GET"])
@token_required
def list():
    return jsonify([product.to_json() for product in product_list()])


@blueprint_product.route("/<int:id>", methods=["GET"])
@token_required
def by_id(id: int):
    product = product_by_id(id)
    if product is None:
        return jsonify({'error': 'Produk tidak ditemukan.'}), 404

    return jsonify(product.to_json()), 200


@blueprint_product.route("/", methods=["POST"])
@token_required
def create():
    data = request.json
    product = product_create(
        title=data.get('title'),
        description=data.get('description'),
        priority=data.get('priority'),
        due_date=data.get('due_date')
    )
    if product is None:
        return jsonify({'error': 'Inputan invalid.'}), 400
    return jsonify(product.to_json()), 200


@blueprint_product.route("/<int:id>", methods=["PUT"])
@token_required
def update(id: int):
    product = product_by_id(id)
    if product is None:
        return jsonify({'error': 'Produk tidak ditemukan.'}), 404

    data = request.json
    product_updated = product_update(
        product=product,
        title=data.get('title'),
        description=data.get('description'),
        priority=data.get('priority'),
        due_date=data.get('due_date')
    )
    if product_updated is None:
        return jsonify({'error': 'Inputan invalid.'}), 400
    return jsonify(product_updated.to_json()), 200


@blueprint_product.route("/<int:id>", methods=["DELETE"])
@token_required
def delete(id: int):
    product = product_by_id(id)
    if product is None:
        return jsonify({'error': 'Produk tidak ditemukan.'}), 404

    if product_delete(product):
        return '', 200

    return jsonify({'error': 'Inputan invalid.'}), 400
