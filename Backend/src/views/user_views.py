from flask import request,Blueprint
from src.extension import db
from src.helpers import *


users_end = Blueprint('Users', __name__,url_prefix="/users_end")

@users_end.route('/')
def user_end():
    return "Hello from my users_end"

@users_end.route('/sign_up',methods=["POST"])
def sign_up():
    #signup new users 
    data = request.get_json()#get_users_details 
    return create_user(data)

@users_end.route('/login',methods=["POST"])
def login():
    #login existing users with the mobile number
    data = request.get_json()

    return user_login(data)


@users_end.route('/logout',methods=["POST"])
def logout():
    # Clear session variables
    session.pop('logged_in', None)
    session.pop('user_id', None)

    return {"message": "user logged out"}

@users_end.route('/get_user_data',methods=["GET"])
def get_user_data():
    data = request.get_json()
    user_data=get_user_data_id(**data)
    return user_data

@users_end.route('/recommendations',methods=["POST"])
def recommendations():
    user_recommendations=get_user_recommendations()
    return user_recommendations


@users_end.route('/session_parameters',methods=["GET"])
def session_params():

    return {"message": session}