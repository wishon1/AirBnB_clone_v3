#!/usr/bin/python3
""" index.py file of our flask application """

# from api.v1.views import app_views
from . import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Checks the status and returns a json"""
    data = {
            "status": "OK"
            }
    return jsonify(data)


@app_views.route('/stats', methods=['GET'])
def retrieve_number():
    """
    Create an endpoint that retrieves the number of each objects by type:
    """
    response = {}
    objects = {
            "Amenity": "iamenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for key, value in objects.items():
        response[value] = storage.count(key)
    return jsonify(response)
