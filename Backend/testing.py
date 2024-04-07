data=[{"user_id1":3,"user_id2":1,"Consc":7.168,"Agree":17.5,"total":0.048863,"Open":6.3,"id":2,"Extrav":12.348,"Neuro":5.547},
      {"user_id1":2,"user_id2":3,"Consc":6.272,"Agree":3.9,"total":0.03128,"Open":6.51,"id":3,"Extrav":11.76,"Neuro":2.838}]

import pandas as pd

data=pd.DataFrame(data)
print(data)
from src.helpers import get_user_data_id

u=3
compatable_users=[]
for index,x in data.iterrows():
    d={"user_id":None,"score":None,"name":None,"gender":None}

    if x["user_id1"] != u:
        d["user_id"]=x["user_id1"]  
    else:
        d["user_id"]=(x['user_id2'])

    d["score"]=x["total"]
    # user_data=get_user_data_id(d["user_id"])
    # d["name"]=user_data["name"]
    # d["gender"]=user_data["gender"]
    compatable_users.append(d)
print(compatable_users)


# for index,row in data.iterrows():
#     print(index,row["user_id1"])