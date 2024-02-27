#!/usr/bin/python3
'''
index.py file of our flask application
adding more documentation to the index file
'''

# from api.v1.views import app_views
from . import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    '''
    Checks the status and returns a json
    This function is run and returns a json file showing status okay
    this is done in json
    '''
    data = {
            "status": "OK"
            }
    return jsonify(data)


@app_views.route('/stats', methods=['GET'])
def retrieve_number():
    '''
    Create an endpoint that retrieves the number of each objects by type
    This shows the stats we have in the database
    '''
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
