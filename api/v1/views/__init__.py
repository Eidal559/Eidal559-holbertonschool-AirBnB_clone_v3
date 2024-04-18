#!/usr/bin/python3
""" Creates the app_views template"""
from flask import Blueprint

# Creates a Blueprint which the rest of our pages will run through
app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

# Must import individual files below so as not to circular import
from api.v1.views.index import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
