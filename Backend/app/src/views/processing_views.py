""" These are the processing views mainly used for processing of the user data.
    It takes the test score of the users , stores it in the database and returns the recommendations"""


from flask import request, Blueprint
from src.extension import db
from src.helpers import *
from flask import jsonify

process_end = Blueprint("Process", __name__, url_prefix="/process_end")


@process_end.route("/")
def process_endpoint():
    return "Hello from my process_end"


@process_end.route("/test_score", methods=["POST"])
def test_score():
    """This function is used to post the test score of the user"""
    data = request.get_json()
    result = test_score_to_db(data)
    return jsonify(result)
