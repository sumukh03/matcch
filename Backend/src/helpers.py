from .db_utils import *


def create_user(data):
    """Checks if all the required fields are present to create the user
    if required fields are missing return that 
    else create the user and return the user_id"""

    #checking the fields 
    required_fields=get_fields_table("User")
    required_fields.remove("user_id")

    #if required_fields != received_data , return the required/missing field
    if sorted(data.keys()) != sorted(required_fields):
        return required_fields.pop(data.keys())
    
    return Insert_table("Users",data)

def get_user_mobile():
    pass