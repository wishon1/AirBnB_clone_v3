#!/usr/bin/python3
"""This is the Amenity view. We will handle the common api actions"""

from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def retrieve_all_amenities():
    """This function returns all amenities"""
    object_amenity = []
    all_amenities = storage.all("Amenity")
    for obj in all_amenities.values():
        object_amenity.append(obj.to_dict())
    return jsonify(object_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_amenity_id(amenity_id):
    """Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>"""
    amenity_object = storage.get("Amenity", str(amenity_id))
    if amenity_object is None:
        abort(404)
    return jsonify(amenity_object.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>"""
    amenity_to_delete = storage.get("Amenity", str(amenity_id))
    if amenity_to_delete is None:
        abort(404)
    storage.delete(amenity_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a Amenity: POST /api/v1/amenities"""
    amenity_to_create = request.get_json(silent=True)
    if amenity_to_create is None:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_to_create:
        abort(400, 'Missing name')
    created_amenity = Amenity(**amenity_to_create)
    created_amenity.save()
    response = jsonify(created_amenity.to_dict())
    response.status_code = 201
    return response


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>"""
    amenity_to_update = storage.get(Amenity, str(amenity_id))
    if amenity_to_update is None:
        abort(404)
    amenity_update = request.get_json(silent=True)
    if amenity_update is None:
        abort(400, 'Not a JSON')
    for key, value in amenity_update.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_to_update, key, value)
    amenity_to_update.save()
    return jsonify(amenity_to_update.to_dict()), 200
