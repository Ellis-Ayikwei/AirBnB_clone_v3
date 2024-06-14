from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity



@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """function to show the ameities with the amenity route"""
    amenities = storage.all('Amenity')
    return jsonify([amenity.to_dict() for amenity in amenities.values()])

@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """function to show the amenity with the amenity_id  route"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """function to delete cities with the amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity_id:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create an amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    req_data = request.get_json()
    amenity.name = req_data['name']
    amenity.save()
    return jsonify(amenity.to_dict()), 200
