#!/usr/bin/python3
from  api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """
    Route to return a JSON object with a status of 'OK'.

    Returns:
        JSON: A JSON object with a single key-value pair, where the key is 'status'
              and the value is 'OK'.
    """
    # Create a dictionary with a single key-value pair, where the key is 'status'
    # and the value is 'OK'.
    return_dict = {'status': 'OK'}

    # Convert the dictionary to a JSON object and return it.
    return jsonify(return_dict)
