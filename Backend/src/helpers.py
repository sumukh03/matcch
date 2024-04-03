from .extension import session
from src.extension import db
from .db_utils import *
""" 1.read csvs
    2.conver the scored to keys ("A")
    3.calculate compatability score  """

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
        return {"message":"User Found ","user_id":result[0]['user_id']}
    else:
        return {"message":"Passowod incorrect"}

def get_user_data(columns,values):
    condition={"column":columns,"value":values}
    return Select_table("users",condition)
    
def get_user_data_id(user_id):
    condition={"column":["user_id"],"value":[user_id]}
    return Select_table("users",condition)[0]

def calculate_compatability(user_id) :
    order_vector=("Open","Consc","Extrav","Agree","Neuro")
    def dict_to_order_vec(data):
        res=[]
        for key in order_vector:
            res.append(data[key])

        return tuple(res)
    
    def get_user_score_vector(user_id):
        condition={"column":["user_id"],"value":[user_id]}

        user_scores= Select_table("user_score",condition)[0]

        user_scores=dict_to_order_vec(user_scores)

        user_score_vector=convert_score(user_scores)

        return user_scores,user_score_vector
    
    def get_compatability_csvs():
        import os
        BASE_PATH="src/csvs"
        oc=pd.read_csv(os.path.join(BASE_PATH,"openness_compatability.csv"),index_col=0)
        cc=pd.read_csv(os.path.join(BASE_PATH,"conscientiousness_compatability.csv"),index_col=0)
        ec=pd.read_csv(os.path.join(BASE_PATH,"extraversion_compatability.csv"),index_col=0)
        ac=pd.read_csv(os.path.join(BASE_PATH,"agreeableness_compatability.csv"),index_col=0)
        nc=pd.read_csv(os.path.join(BASE_PATH,"neuroticism_compatability.csv"),index_col=0)
        return [oc,cc,ec,ac,nc]
    
                     
    user_scores,user_score_vector=get_user_score_vector(user_id)
    compatibility_data=get_compatability_csvs()

    condition={"column":[],"value":[]}

    for row in Select_table("user_score",condition):
        if row["user_id"]!=user_id:
            u_scores,u_score_vector=get_user_score_vector(row["user_id"])
            compatibility_users=[]
            idx=0
            for x,y in zip(user_score_vector,u_score_vector):
                compatibility_users.append(compatibility_data[idx][x][y]*user_scores[idx]*u_scores[idx]/1000)
                idx+=1

            fields=get_fields_table("compatibility")
            for key,value in zip(order_vector,compatibility_users):
                fields[key]=value
            fields["user_id1"]=user_id
            fields["user_id2"]=row["user_id"]
            fields.pop("id",None)
            fields["total"]=sum(compatibility_users)/1000
            id=Insert_table("compatibility",[fields])
            if not id :
                return "ERROR"
    return True
                
    

def convert_score(data):
    res=[]

    for v in data:
        value=2*int(v)
        if value >= 90:
            res.append('A')
        elif value >= 80:
            res.append('B')
        elif value >= 70:
            res.append('C')
        elif value >= 60:
            res.append('D')
        elif value >= 50:
            res.append('E')
        elif value >= 40:
            res.append('F')
        elif value >= 30:
            res.append('G')
        elif value >= 20:
            res.append('H')
        elif value >= 10:
            res.append('I')
        else:
            res.append('J')
    return tuple(res)

def test_score_to_db(data):

    if session.get("logged_in",None):
        required_fields=get_fields_table("user_score")
        required_fields["user_id"]=session["user_id"]
        required_fields.update(data)
        id=Insert_table("user_score",[required_fields])

        #get all the records and modify the compatability 
        cal=calculate_compatability(session["user_id"])

        if id and cal :
            return "Score posted"
        else:
            return "failed"
            

    return "Please Login or signup"
    


def get_user_recommendations():
    user_id=session.get("user_id",None)
    if session.get("logged_in",None) and user_id :
        condition={"column":["user_id1"],"value":[user_id]}
        rows=Select_table("compatibility",condition)
        
        condition={"column":["user_id2"],"value":[user_id]}
        other_rows=Select_table("compatibility",condition)
        if other_rows:
            rows.append(other_rows)

        df=pd.DataFrame(rows)
        df=df.sort_values(by='total',ascending=False)
        df = df.to_json(orient='records')
        return df
    return "Please Login or signup"



#for retest , just delete the rows from compatibility table and , again do test_scores_to_db