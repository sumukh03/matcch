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
    
    if result["password"]==data["password"]:
        return {"message":"User Found"}
    else:
        return {"message":"Passowod incorrect"}

def get_user_data(columns,values):
    condition={"column":columns,"value":values}
    return Select_table("users",condition)
    