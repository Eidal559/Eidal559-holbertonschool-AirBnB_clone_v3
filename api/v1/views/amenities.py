#!/usr/bin/python3
"""Module amenities - handles amenities objects for RESTful API."""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    all_amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in all_amenities]
    return make_response(jsonify(list_amenities), 200)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new Amenity object."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an existing Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
