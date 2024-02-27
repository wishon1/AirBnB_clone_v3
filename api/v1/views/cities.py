#!/usr/bin/python3

"""
City view module for handling RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.city import City as Cty


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def state_cities(state_id):
    """ Retrieve cities of a specific state """
    # Get all states
    states = storage.all('State').values()
    # Check if the state exists
    state_found = any(state.id == state_id for state in states)
    if not state_found:
        abort(404)
    # Create a list of dictionaries containing city information
    # for the specified state
    cities_list = [city.to_dict() for city in storage.all('City').values()
                   if city.state_id == state_id]
    # Return the cities list in JSON format
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ Get city by its ID """
    # Find the city with the specified ID
    city = next((city for city in storage.all('City').values()
                 if city.id == city_id), None)
    # If city not found, return 404 error
    if not city:
        abort(404)
    # Return the city information in JSON format
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Delete city by its ID """
    # Find the city with the specified ID
    city = next((city for city in storage.all('City').values()
                 if city.id == city_id), None)
    # If city not found, return 404 error
    if not city:
        abort(404)
    # Delete the city from the database
    storage.delete(city)
    storage.save()
    # Return empty response with 200 status code
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """ Add a new city to a specific state """
    # Get all states
    states = storage.all('State').values()
    # Check if the state exists
    state_found = any(state.id == state_id for state in states)
    if not state_found:
        abort(404)
    # Check if request contains JSON data
    if not request.json:
        abort(400, "No JSON content")
    # Check if 'name' attribute is in the JSON data
    if "name" not in request.json:
        abort(400, "Missing 'name' attribute")
    # Add the state ID to the JSON data
    data = request.get_json()
    data['state_id'] = state_id
    # Create a new city object with the JSON data
    new_city = Cty(**data)
    new_city.save()
    # Return the new city information in JSON format with 201 status code
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Update city by its ID """
    # Check if request contains JSON data
    if not request.json:
        abort(400, "No JSON content")
    # Define keys to be ignored during update
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    # Find the city with the specified ID
    city = next((city for city in storage.all('City').values()
                 if city.id == city_id), None)
    # If city not found, return 404 error
    if not city:
        abort(404)
    # Update city attributes with the JSON data
    for k, v in request.json.items():
        if k not in ignored_keys:
            setattr(city, k, v)
    # Save the updated city object
    city.save()
    # Return the updated city information in JSON format
    return jsonify(city.to_dict())
