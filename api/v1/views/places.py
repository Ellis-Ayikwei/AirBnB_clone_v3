#!/usr/bin/python3
"""The place view"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places', methods=['GET'],
                 strict_slashes=False)
def places():
    """function to show the ameities with the place route"""
    places = storage.all('Place')
    return jsonify([place.to_dict() for place in places.values()])


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
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
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get(City, c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_dict() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get(Amenity, a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_dict() for place in places_amenities]
    return jsonify(result)