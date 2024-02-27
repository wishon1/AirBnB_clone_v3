#!/usr/bin/python3
"""
Create a view for city
"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrieve_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    # Retrieve the state object with the given state_id from the database
    target_state = storage.get("State", state_id)

    # If state is not found, return 404 error
    if not target_state:
        abort(404)
    # Retrieve all City objects associated with the State object
    city_objects = target_state.cities

    # Convert City objects to dictionaries using to_dict() method
    city_list = [city.to_dict() for city in city_objects]

    # Return the list of City objects as JSON
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """Retrieves a City object by ID"""
    # Retrieve the city object with the given city_id from the database
    target_city = storage.get("City", city_id)

    # If city is not found, return 404 error
    if not target_city:
        abort(404)

    # Return the city object as JSON
    return jsonify(target_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by ID"""
    # Retrieve the city object with the given city_id from the database
    target_city = storage.get("City", city_id)

    # If city is not found, return 404 error
    if not target_city:
        abort(404)

    # Delete the city object from the database
    target_city.delete()
    storage.save()

    # Return an empty dictionary with status code 200
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city"""
    # Retrieve the state object with the given state_id from the database
    target_state = storage.get("State", state_id)

    # If state is not found, return 404 error
    if not target_state:
        abort(404)

    # Get the JSON data from the request
    new_city_data = request.get_json()

    # If JSON data is not valid, return 400 error
    if not new_city_data:
        abort(400, 'Not a JSON')

    # If 'name' key is missing in JSON data, return 400 error
    if 'name' not in new_city_data:
        abort(400, 'Missing name')
    # Create a new City object using the JSON data
    new_city = City(**new_city_data)

    # Set the state_id attribute of the new city object
    setattr(new_city, 'state_id', state_id)

    # Add the new city object to the database
    storage.new(new_city)
    storage.save()

    # Return the new city object as JSON with status code 201
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object by ID"""
    # Retrieve the city object with the given city_id from the database
    target_city = storage.get("City", city_id)

    # If city is not found, return 404 error
    if not target_city:
        abort(404)
    # Get the JSON data from the request
    update_data = request.get_json()

    # If JSON data is not valid, return 400 error
    if not update_data:
        abort(400, 'Not a JSON')

    # Update the City object's attributes based on the JSON data
    for key, value in update_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(target_city, key, value)
    # Save the changes to the database
    storage.save()

    # Return the updated city object as JSON with status code 200
    return make_response(jsonify(target_city.to_dict()), 200)
