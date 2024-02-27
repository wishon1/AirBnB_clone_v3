#!/usr/bin/python3
"""
Create a new view for User object that handles
all default RESTFul API actions
"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
def retrieve_all_users():
    """This function retrieves the list of all users"""
    objects = []
    all_users = storage.all("User")
    for obj in all_users.values():
        objects.append(obj.to_dict())
    return jsonify(objects)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def retriving_single_user(user_id):
    """Retrieves a single user depending on the id passed"""
    all_users = storage.all("User")
    for obj in all_users.values():
        if obj.id == user_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object:: DELETE /api/v1/users/<user_id>"""
    user_to_delete = storage.get("User", str(user_id))
    if user_to_delete is None:
        abort(404)
    storage.delete(user_to_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User: POST /api/v1/users"""
    user_to_create = request.get_json(silent=True)
    if user_to_create is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_to_create:
        abort(400, 'Missing email')
    if 'password' not in user_to_create:
        abort(400, 'Missing password')
    created_user = User(**user_to_create)
    created_user.save()
    response = jsonify(created_user.to_dict())
    response.status_code = 201
    return response


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object: PUT /api/v1/users/<user_id>"""
    user_to_update = storage.get(User, str(user_id))
    if user_to_update is None:
        abort(404)
    user_update = request.get_json(silent=True)
    if user_update is None:
        abort(400, 'Not a JSON')
    for key, value in user_update.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user_to_update, key, value)
    user_to_update.save()
    return jsonify(user_to_update.to_dict()), 200
