from flask import request,Blueprint
from src.helpers import *


users_end = Blueprint('Users', __name__,url_prefix="/users_end")

@users_end.route('/')
def user_end():
    return "Hello from my users_end"

@users_end.route('/sign_up',methods=["POST"])
def sign_up():
    #signup new users 
    data = request.get_json()
    #get_users_details 
    # get_user_mobile(data["mobile"])
    print(data)
    #check if mobile exists 
    flag=create_user(data)
    return "Hello from my users_end{}".format(flag)

@users_end.route('/login',methods=["POST"])
def login():
    #signup new users 
    # flag=user_login()
    return "Hello from my users_end"