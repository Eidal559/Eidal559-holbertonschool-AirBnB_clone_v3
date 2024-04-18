#!/usr/bin/python3
"""Module amenities - handles Amenity objects for RESTful API."""
from models import amenity
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves a list of all Amenity objects."""
    all_amenities = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(list_amenities), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)


if amenity is None:
    abort(404)

storage.delete(amenity)
storage.save()


def delete_amenity():
    return jsonify({}), 200


delete_amenity()


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity object."""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a specific Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    storage.save()

    return jsonify(amenity.to_dict()), 200
