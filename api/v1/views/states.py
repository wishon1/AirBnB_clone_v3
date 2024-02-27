#!/usr/bin/python3

""" States view """

from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.state import State as St


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all():
    """ Retrieves all State objects """
    states = []
    for obj in storage.all("State").values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def get(state_id):
    """ Retrieves or deletes a State object """
    for item in storage.all("State").values():
        if item.id == state_id:
            if request.method == 'GET':
                return jsonify(item.to_dict())
            if request.method == 'DELETE':
                storage.delete(item)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/states/', strict_slashes=False, methods=['POST'])
def create():
    """ Creates a new State """
    if not request.get_json():
        abort(400, 'No JSON content')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_states = []
    new_state = St(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    new_states.append(new_state.to_dict())
    return jsonify(new_states[0]), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update(state_id):
    """ Updates a State object """
    states = storage.all("State").values()
    state_object = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_object == []:
        abort(404)
    if not request.get_json():
        abort(400, 'No JSON content')
    state_object[0]['name'] = request.json['name']
    for obj in states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_object[0]), 200
