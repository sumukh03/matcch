""" This file contains the user views 
    It contains functions to create users, get the recommendation based on the user_id"""

from flask import request, Blueprint
from src.extension import db
from src.helpers import *
from flask import jsonify

users_end = Blueprint("Users", __name__, url_prefix="/users_end")


@users_end.route("/")
def user_end():
    return "Hello from my users_end"


@users_end.route("/details", methods=["POST"])
def sign_up():
    """This method is used to post the new user details
    This ACCEPTS the mobile number of the user
    This method RETURNS the user_id of the newly created user"""
    data = request.get_json()
    return jsonify(create_user(data))


@users_end.route("/recommendations", methods=["POST"])
def recommendations():
    """This endpoint is used to get the recommendations for the user
    ACCEPTS the user_id
    RETURNS the user recommendations"""
    data = request.get_json()
    user_recommendations = get_user_recommendations(data)
    return jsonify(user_recommendations)


@users_end.route("/get_user_details", methods=["POST"])
def user_details():
    """This end point is used to get the user_details using the user_id
    This ACCEPTS the user_id
    RETURNS the user details"""
    data = request.get_json()
    resp = get_user_data_id(data["user_id"])
    return jsonify(resp)
