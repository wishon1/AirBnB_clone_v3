#!/usr/bin/python3
"""
Create a new view for State objects that handles all default
RESTful API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_states():
    """ Retrieve all the lists of states objects into json"""
    # Retrieve all states from the database
    all_states = storage.all(state.State)

    # Convert states to dictionaries and put them in a list
    state_list = [state.to_dict() for state in all_states.values()]

    # Return the list of states as JSON
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieve a state object"""
    # Retrieve the state with the given state_id from the database
    state_obj = storage.get(state.State, state_id)

    # If state is not found, return 404 error
    if state_obj is None:
        abort(404)

    # Return the state as JSON
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State: DELETE /api/v1/states/<state_id>"""
    # Retrieve the state with the given state_id from the database
    state_obj = storage.get(state.State, state_id)

    # If state is not found, return 404 error
    if state_obj is None:
        abort(404)

    # Delete the state from the database
    storage.delete(state_obj)
    storage.save()

    # Return an empty response with status code 200
    return jsonify({})


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a State: POST /api/v1/states"""
    # Get the JSON data from the request
    json_data = request.get_json()

    # If JSON data is not valid, return 400 error
    if json_data is None:
        abort(400, 'Not a JSON')

    # If 'name' key is missing in JSON data, return 400 error
    if 'name' not in json_data:
        abort(400, 'Missing name')

    # Create a new state object
    new_state = state.State(**json_data)

    # Add the new state to the database
    storage.new(new_state)
    storage.save()

    # Return the new state as JSON with status code 201
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    # Retrieve the state with the given state_id from the database
    state_obj = storage.get(state.State, state_id)

    # If state is not found, return 404 error
    if state_obj is None:
        abort(404)

    # Get the JSON data from the request
    json_data = request.get_json()

    # If JSON data is not valid, return 400 error
    if json_data is None:
        abort(400, 'Not a JSON')

    # Update the state object with the key-value pairs from JSON data
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, key, value)

    # Save the changes to the database
    storage.save()

    # Return the updated state as JSON with status code 200
    return jsonify(state_obj.to_dict()), 200
