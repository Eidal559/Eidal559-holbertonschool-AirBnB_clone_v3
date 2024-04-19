#!/usr/bin/python3
"""Module users - handles user objects for RestfulAPI"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves list of all User objects."""
    all_users = storage.all(User).values()
    list_users = [user.to_dict() for user in all_users]
    return jsonify(list_users), 200


@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific User object by user_id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by user_id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object."""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if 'email' not in data:
        abort(400, description="Missing email")

    if 'password' not in data:
        abort(400, description="Missing password")

    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an existing User object by user_id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
