#!/usr/bin/python3
""" index.py file of our flask application """

# from api.v1.views import app_views
from . import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Checks the status and returns a json"""
    data = {
            "status": "OK"
            }
    return jsonify(data)
