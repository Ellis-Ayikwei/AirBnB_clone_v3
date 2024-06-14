from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

"""import the storage"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

"""import flask views"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *


