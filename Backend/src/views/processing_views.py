from flask import request,Blueprint
from src.extension import db
from src.helpers import *
from flask import jsonify

process_end = Blueprint('Process', __name__,url_prefix="/process_end")

@process_end.route('/')
def process_endpoint():
    return "Hello from my process_end"


@process_end.route('/test_score',methods=["POST"])
def test_score():

    data = request.get_json()
    prep_data=prepare_data(data)
    if prep_data:
        result=test_score_to_db(prep_data)
        return jsonify(result)
    return make_response(None, False,"Could not post Test score")