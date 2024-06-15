#!/usr/bin/python3
"""The place view"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('/places', methods=['GET'],
                 strict_slashes=False)
def places():
    """function to show the ameities with the place route"""
    places = storage.all('Place')
    return jsonify([place.to_dict() for place in places.values()])


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def place(city_id):
    """function to show the city with the city_id  route"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_with_id(place_id):
    """function to show the place with the place_id  route"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """function to delete cities with the place_id"""
    place = storage.get(Place, place_id)
    if not place_id:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_data = request.get_json()
    place_data['city_id'] = city.id
    place = Place(**place_data)
    print(f"the place data {place_data}")
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    req_data = request.get_json()
    place.name = req_data['name']
    place.description = req_data['description']
    place.number_rooms = req_data['number_rooms']
    place.number_bathrooms = req_data['number_bathrooms']
    place.max_guest = req_data['max_guest']
    place.price_by_night = req_data['price_by_night']
    place.latitude = req_data['latitude']
    place.longitude = req_data['longitude']
    place.save()