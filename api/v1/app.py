#!/usr/bin/python3
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """
    Return JSON formatted 404 status code response.

    Args:
        error (Exception): The error that raised the 404.

    Returns:
        Flask response: A JSON response with a 404 status code and a
        message indicating that the requested resource was not found.
    """
    # Create a JSON response with a 404 status code and a message.
    response = make_response(jsonify({'error': 'Not found'}), 404)

    return response


@app.teardown_appcontext
def teardown_db(self):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
