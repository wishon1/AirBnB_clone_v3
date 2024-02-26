#!/usr/bin/python3
"""
Create a new view for State objects that handles all default
RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage, state


@app_views.route('/states', method=['GET'], strict_slashes=False)
def retrieve_states():
    """ Retrieve all the lists of states objects into json"""
    all_states = storage.all(State)
    state_list = []
    for state in all_states:
        
        # convert each state object to dictionary
        state_dic = state.to_dict()
        # append dictionary to the list
        state_list.append(state_dic)
        # convert the list of dictionaries to json response
    json_response = jsonify(state_list)
    return json_response

@app_views.route('/states/<state_id>', method=['GET'],
                 strict_slashes=False)
def get_states():
    """rerieve a state object"""
    # send a request method to get the state id
    state_id_obj = storage.get("State", state_id)
    if state_id_obj is None:
        abort(404)
    dict_format = state_id_obj.to_dict()
    json_format = jsonify(dict_format)
    return json_format

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states():
    """Deletes a State: DELETE /api/v1/states/<state_id>"""
    state_id_obj = storage.get("State", state_id)
    if state is None:
        abort (404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>', methods=['POST'],
                 strict_slashes=False)
def create_states():
    """Creates a State: POST /api/v1/states"""
    # send HTTP request to get the json format of the state
    json_format = request.get_json()
    if json_format is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_format:
        abort(400, 'Missing name')
    # create a new state
    state = State(**json_format)
    storage.new(state)
    storage.save()
    state.to_dict()

    # return an empty dictionary with status code 200
    return make_response(jsonify(state), 201)

@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
    def update_states():
        """Updates a State object: PUT /api/v1/states/<state_id>"""
        state = storage.get("State", state_id)
        if not state:
            abort(404)
        # send a request to get the json format
        json_format = request.get_json()
        if not json_format:
            abort(400, 'Not a JSON')
        
        # Update the State object with the key-value pairs from JSON data
        for key, value in json_format,items():
            if key not in ['id', 'created_at', 'updtated_at']:
                setattr(state, key, value)
        state.save()
        state.to_dict()

        return make_rsponse(jsonify(state), 200)
