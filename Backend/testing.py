from src.db_utils import *
from src.models.user_models import *
# from models.processing_models import *
from src.extension import db

# condition={"column":["mobile"],"value":["960396183"]}
# print(Select_table("users",condition))



d={"a":1,"b":2}
f={'c':"","a":"","b":""}

print(list(d.keys()),type(d.keys()))

print(f.pop(list(d.keys())))