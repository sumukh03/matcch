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
    # signup new users
    data = request.get_json()  # get_users_details
    return jsonify(create_user(data))


@users_end.route("/recommendations", methods=["POST"])
def recommendations():
    data = request.get_json()
    user_recommendations = get_user_recommendations(data)
    return jsonify(user_recommendations)

