#!/usr/bin/python3
"""
Creating a flask application
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
# from app.app_views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_context(exception):
    """
    A tear down function. this runs every
    time the application context is torn down
    """
    storage.close()


@app.errorhandler(404)
def error_handler_404(error):
    """Handler for the 404 error. Returns a json"""
    err = {
            "error": "Not found"
            }
    return jsonify(err), 404


if __name__ == "__main__":
    """
    This is a documentation.
    this function dictates where the code runs
    """
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
