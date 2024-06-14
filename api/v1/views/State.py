from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """function to show the states with the state route"""
    states = storage.all('State')
    return jsonify([state.to_dict() for state in states.values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state(state_id):
    """function to show the state with the state_id  route"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_states(state_id):
    """function to delete states with the state_id"""
    state = storage.get(State, state_id)
    if not state_id:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200 


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    
    state = storage.get(State, state_id )
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    req_data = request.get_json()
    state.name = req_data['name']
    state.save()
    return jsonify(state.to_dict()), 200
