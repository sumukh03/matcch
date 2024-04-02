from .extension import session
from src.extension import db
from .db_utils import *


def create_user(data):
    """Checks if all the required fields are present to create the user
    if required fields are missing return that 
    else create the user and return the user_id"""

    if get_user_data(columns=["mobile"],values=[data["mobile"]]):
        return {"message":"Mobile already exists! Please login"}
    #check if mobile exists 
    else:
        #checking the fields 
        required_fields=get_fields_table("users")
        required_fields.update(data)
        required_fields.pop("user_id",None)
        #if required_fields != received_data , return the required/missing field
        keys=data.keys()
        missing=[]
        for k in required_fields.keys():
            if k not in keys:
                missing.append(k)
        if missing:
            return {"message":f"Missing fields -- {missing}"}
        
        id= Insert_table("users",[required_fields])
        if id:
            return {"message":"User Created"}
        else:
            return {"message":"User Cannot be Created"}

def user_login(data):

    result=get_user_data(columns=["mobile"],values=[data["mobile"]])

    if not result:
        return {"message":"Mobile DOES NOT exists! Please Sign-up"}
    
    if result[0]["password"]==data["password"]:
        session['logged_in'] = True
        session['user_id'] = result[0]["user_id"]
        return {"message":"User Found user_id={} ".format(result[0]['user_id'])}
    else:
        return {"message":"Passowod incorrect"}

def get_user_data(columns,values):
    condition={"column":columns,"value":values}
    return Select_table("users",condition)
    


def test_score_to_db(data):

    if session.get("logged_in",None):
        required_fields=get_fields_table("user_score")
        required_fields["user_id"]=session["user_id"]
        data.update(required_fields)
        id=Insert_table("user_score",[data])

        if id:
            return "Score posted"
        else:
            return "failed"
            

    return "Please Login or signup"
    

