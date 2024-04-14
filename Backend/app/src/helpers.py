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
    return {"data": data, "status": status, "message": message}


def create_user(data):
    """This function creates the new user
    It ACCEPTS the mobile number and
    IT RETURNS the user_id of the new user"""
    insert_initial_data()
    if data.get("mobile", None):
        id = Insert_table("users", [{"mobile": data["mobile"]}])
        if id:
            condition = {"column": ["mobile"], "value": [data["mobile"]]}
            user_data = Select_table("users", condition)[-1]
            return make_response(user_data["user_id"], True, "User Created")
        else:
            return make_response(id, False, "User could not be Created")
    return make_response(id, False, f"Please enter Mobile number")


def get_user_data(columns, values):
    """This function is used to get the user data from the database based on the condition"""
    condition = {"column": columns, "value": values}
    return Select_table("users", condition)


def get_user_data_id(user_id):
    """This function is used to get the user data based on the user_id"""
    condition = {"column": ["user_id"], "value": [user_id]}
    return Select_table("users", condition)


order_vector = ("Open", "Consc", "Extrav", "Agree", "Neuro")


def dict_to_order_vec(data):
    """This function is used to order the scores into a vector"""
    res = []
    for key in order_vector:
        res.append(data[key])

    return res


def get_user_score(user_id):
    condition = {"column": ["user_id"], "value": [user_id]}

    user_score = Select_table("user_score", condition)[0]

    user_score = dict_to_order_vec(user_score)

    return user_score


def find_compatible_vectors(user_id):
    """This function ACCEPTS the user_id
    it gets the user_score vector from the database
    it classifies the user into one of the cluster
    it then finds the similar vectors based on the linear distance
    RETURNS the list of compatible users from the database"""

    query_vector = get_user_score(user_id)
    cluster_label = kmeans.predict([query_vector])[0]

    cluster_indices = np.where(kmeans.labels_ == cluster_label)[0]
    cluster_indices = tuple(map(int, cluster_indices))

    similar_vectors = [get_user_score(idx) for idx in cluster_indices]

    distances = [
        np.linalg.norm(np.array(query_vector) - np.array(v)) for v in similar_vectors
    ]

    sorted_indices = list(map(int, np.argsort(distances)))

    compatible_users = {}

    for i in sorted_indices[:5]:
        compatible_users[cluster_indices[i]] = similar_vectors[int(i)]

    return compatible_users


def convert_score(data):
    """This function is used to convert the user_score vector to the resultant grade vector
    to get the compatibility scores"""
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
        scores = calc_from_rawData(data["answers"])

        required_fields = get_fields_table("user_score")
        required_fields["user_id"] = data["user_id"]
        required_fields.update(scores)
        required_fields.pop("id")

        id = Insert_table("user_score", [required_fields])

        if id:
            return get_user_recommendations({"user_id": data["user_id"]})
        else:
            return make_response(None, False, "Score not posted")

    return make_response(None, False, "Please enter the user_id")


def make_recommendations_data(user_id, compatable_users):
    """This function is used to get the compatability points of the similar users
    It ACCEPTS the user_id of the current user and the scores of the compatable users
    It RETURNS the compatable users along with the compatability points"""

    def get_compatability_csvs():
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

    user_data = get_user_score(user_id)
    user_data_vector = convert_score(user_data)

    compatable_vectors = {}

    csvs = get_compatability_csvs()

    for key, value in compatable_users.items():
        value_vector = convert_score(value)

        idx = 0
        l = []

        for x, y in zip(value_vector, user_data_vector):
            l.append(csvs[idx][x][y])
            idx += 1
        compatable_vectors[key] = l

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
        compatable_users = find_compatible_vectors(user_id)
        final_compatable = make_recommendations_data(user_id, compatable_users)

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
    condition = {"column": ["user_id"], "value": [5000]}
    if not Select_table("user_score", condition):
        data = pd.read_json("src/datasets/data.json")
        l = []
        for i in range(1, len(data) + 1):
            l.append({"mobile": i})
        ids = Insert_table("users", l)

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

        Insert_df(data)
