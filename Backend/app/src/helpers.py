from src.extension import db
from .db_utils import *
import joblib
import numpy as np


def get_kmeans_model():
    """This function is to load the kmeans model"""
    file_path = "src/kmeans_model_5000.pkl"
    loaded_model = joblib.load(file_path)
    return loaded_model


kmeans = get_kmeans_model()


def make_response(data, status, message):
    """This funciton is used to format the data that is to be sent through the API"""
    return {"data": data, "status": status, "message": message}


def create_user(data):
    """This function creates the new user
    It ACCEPTS the mobile number and
    IT RETURNS the user_id of the new user"""
    insert_initial_data() # before the first user is created , Initialise the database with the training data
    if data.get("mobile", None):
        id = Insert_table("users", [{"mobile": data["mobile"]}])
        if id:
            #if user data is entered ,return user_id
            condition = {"column": ["mobile"], "value": [data["mobile"]]}
            user_data = Select_table("users", condition)[-1] #select the user_id of the newly created user
            return make_response(user_data["user_id"], True, "User Created") #status =True
        else:
            #if the insert fails , return the error , with status=False
            return make_response(id, False, "User could not be Created") 
    #if missing the mobile number field , ask for mobile number , status =False
    return make_response(id, False, f"Please enter Mobile number")


def get_user_data(columns, values):
    """This function is used to get the user data from the database based on the condition"""
    condition = {"column": columns, "value": values}
    return Select_table("users", condition)


def get_user_data_id(user_id):
    """This function is used to get the user data based on the user_id"""
    condition = {"column": ["user_id"], "value": [user_id]}
    return Select_table("users", condition)


#the order of the of the score vector
order_vector = ("Open", "Consc", "Extrav", "Agree", "Neuro")


def dict_to_order_vec(data):
    """ This function is used to order the scores into a vector
        This takes the dictionary of the user score and converts it to an ordered vector"""
    res = []
    for key in order_vector:
        res.append(data[key])

    return res


def get_user_score(user_id):
    """This function is used to get the user_score vector by taking the user_id as the input"""
    condition = {"column": ["user_id"], "value": [user_id]}

    user_score = Select_table("user_score", condition)[0]#get the user_score from the database

    user_score = dict_to_order_vec(user_score) #convert the score to ordered vector

    return user_score


def find_compatible_vectors(user_id):
    """This function ACCEPTS the user_id
    it gets the user_score vector from the database
    it classifies the user into one of the CLUSTERS
    it then finds the similar vectors based on the LINEAR DISTANCE
    RETURNS the list of compatible users from the database"""

    query_vector = get_user_score(user_id) #getting the ordered score vector of the user (query vector)
    cluster_label = kmeans.predict([query_vector])[0] #predicting the cluster that the user belongs to 

    cluster_indices = np.where(kmeans.labels_ == cluster_label)[0] #getting the id's of the users (neighbours) in that cluster 
    cluster_indices = tuple(map(int, cluster_indices)) 

    similar_vectors = [get_user_score(idx) for idx in cluster_indices] #getting the ordered score vectors of the neighbour users

    distances = [
        np.linalg.norm(np.array(query_vector) - np.array(v)) for v in similar_vectors
    ] #finding the linear distance between the query vector and the neighbour vectors

    sorted_indices = list(map(int, np.argsort(distances))) #sorting the users based on the distance (similarity)

    compatible_users = {}

    for i in sorted_indices[:5]:
        #from the similar user vectors , choosing the top five similar vectors to the query vector
        compatible_users[cluster_indices[i]] = similar_vectors[int(i)] 

    return compatible_users


def convert_score(data):
    """The user scores are converted to grades to get the compatibility scores """
    res = []

    for v in data:
        value = 2 * int(v)
        if value >= 90:
            res.append("A")
        elif value >= 80:
            res.append("B")
        elif value >= 70:
            res.append("C")
        elif value >= 60:
            res.append("D")
        elif value >= 50:
            res.append("E")
        elif value >= 40:
            res.append("F")
        elif value >= 30:
            res.append("G")
        elif value >= 20:
            res.append("H")
        elif value >= 10:
            res.append("I")
        else:
            res.append("J")
    return tuple(res)


def test_score_to_db(data):
    """This funciton is used process the raw test score of the user
    and store it to the database
    RETURNS the recommended users"""

    if data.get("user_id", None):
        scores = calc_from_rawData(data["answers"]) #the raw test answers data is converted to score vector of the user

        required_fields = get_fields_table("user_score") #we get the fields required to insert the new score into the Database
        required_fields["user_id"] = data["user_id"]
        required_fields.update(scores)
        required_fields.pop("id") #removing the primary key ,as it auto-increments

        id = Insert_table("user_score", [required_fields])

        if id:
            return get_user_recommendations({"user_id": data["user_id"]})
        else:
            return make_response(None, False, "Score not posted")

    return make_response(None, False, "Please enter the user_id")


def make_recommendations_data(user_id, compatable_users):
    """Function to get the compatability points of similar users
    It ACCEPTS the user_id of the current user and the scores of the compatable users
    It RETURNS the compatable users along with the compatability points
    """

    def get_compatability_csvs():
        """Function to load the compatibility data from the .csv files"""
        import os

        BASE_PATH = "src/datasets"
        oc = pd.read_csv(
            os.path.join(BASE_PATH, "openness_compatability.csv"), index_col=0
        )
        cc = pd.read_csv(
            os.path.join(BASE_PATH, "conscientiousness_compatability.csv"), index_col=0
        )
        ec = pd.read_csv(
            os.path.join(BASE_PATH, "extraversion_compatability.csv"), index_col=0
        )
        ac = pd.read_csv(
            os.path.join(BASE_PATH, "agreeableness_compatability.csv"), index_col=0
        )
        nc = pd.read_csv(
            os.path.join(BASE_PATH, "neuroticism_compatability.csv"), index_col=0
        )
        return [oc, cc, ec, ac, nc]

    user_data = get_user_score(user_id) #getting the user_score vector
    user_data_vector = convert_score(user_data) #converting the user_score vector to graded vector

    compatable_vectors = {}

    csvs = get_compatability_csvs() #load the compatibility data from the .csv files

    for key, value in compatable_users.items():
        #for every 5 most compatible users 
        value_vector = convert_score(value) #convert the compatable user score to graded vector

        idx = 0
        l = []

        for x, y in zip(value_vector, user_data_vector):
            # for every trait  (i.e. O , C , E , A , N) , find the compatibility points between the user and the neighbour
            l.append(csvs[idx][x][y])
            idx += 1
        compatable_vectors[key] = l

    #adding the compatibility points to the dictionary that we return
    for key, value in compatable_users.items():
        compatable_users[key] = [
            list(map(int, compatable_users[key])),
            list(map(int, compatable_vectors[key])),
        ]

    return compatable_users


def get_user_recommendations(data):
    """This function ACCEPTS the user_id
    RETURNS the compatible users"""
    user_id = data.get("user_id", None)
    if user_id:
        compatable_users = find_compatible_vectors(user_id) #find the neighbour and similar users 
        final_compatable = make_recommendations_data(user_id, compatable_users) #for the the users , add the compatibility points data

        return make_response(final_compatable, True, f"compatibility recommendations ")
    return make_response(None, False, "Please enter user_id")


def calc_from_rawData(answers):
    """this function converts the raw test data to the user_score vector"""
    answers = list(map(int, answers[:50]))

    d = {
        "Extrav": sum(answers[:10]),
        "Neuro": sum(answers[10:20]),
        "Agree": sum(answers[20:30]),
        "Consc": sum(answers[30:40]),
        "Open": sum(answers[40:50]),
    }
    return d


def insert_initial_data():
    condition = {"column": ["user_id"], "value": [5000]} #condition to check if the database has initial data or not
    if not Select_table("user_score", condition):
        data = pd.read_json("src/datasets/data.json")
        l = []
        for i in range(1, len(data) + 1):
            l.append({"mobile": i}) #assigning sequential mobile numbers to the initial user data from the dataset
        ids = Insert_table("users", l) #inserting the user details

        data.rename( 
            columns={
                "O": "Open",
                "C": "Consc",
                "E": "Extrav",
                "A": "Agree",
                "N": "Neuro",
            },
            inplace=True,
        )

        Insert_df(data) #inserting the user score
