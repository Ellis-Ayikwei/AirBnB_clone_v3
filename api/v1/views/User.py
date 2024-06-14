from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User



@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users():
    """function to show the ameities with the user route"""
    users = storage.all('User')
    return jsonify([user.to_dict() for user in users.values()])

@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user(user_id):
    """function to show the user with the user_id  route"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """function to delete cities with the user_id"""
    user = storage.get(User, user_id)
    if not user_id:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a user"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    req_data = request.get_json()
    to_ignore = ("id", "email", "created_at", "updated_at")
    for k in req_data.keys():
        if k in to_ignore:
            pass
        else:
            setattr(user, k, req_data[k])
    user.save()
    return jsonify(user.to_dict()), 200
