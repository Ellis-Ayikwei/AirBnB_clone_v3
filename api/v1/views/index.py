#!/usr/bin/python3
"""
api to show the status and the not found
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    Route to return a JSON object with a status of 'OK'.

    Returns:
        JSON: A JSON object with a single key-value pair,
        where the key is 'status'
              and the value is 'OK'.
    """
    # Create a dictionary with a single key-value pair,
    # where the key is 'status'
    # and the value is 'OK'.
    return_dict = {'status': 'OK'}

    # Convert the dictionary to a JSON object and return it.
    return jsonify(return_dict)


@app_views.route("/stats")
def storage_counts():
    '''
        return counts of all classes in storage
    '''
    cls_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_counts)
