from .extension import session
from src.extension import db
from .db_utils import *
import joblib
import numpy as np


def get_kmeans_model():
    file_path = "src/kmeans_model_5000.pkl"
    loaded_model = joblib.load(file_path)
    return loaded_model


kmeans = get_kmeans_model()


def make_response(data, status, message):
    return {"data": data, "status": status, "message": message}


def create_user(data):
    insert_initial_data()
    if data.get("mobile", None):
        id = Insert_table("users", [{"mobile": data["mobile"]}])
        if id:
            condition = {"column": ["mobile"], "value": [data["mobile"]]}
            user_data = Select_table("users", condition)[0]
            session["logged_in"] = True
            session["user_id"] = user_data["user_id"]
            return make_response(None, True, "User Created")
        else:
            return make_response(None, False, "User could not be Created")
    return make_response(None, False, f"Please enter Mobile number")


def get_user_data(columns, values):
    condition = {"column": columns, "value": values}
    return Select_table("users", condition)


def get_user_data_id(user_id):
    condition = {"column": ["user_id"], "value": [user_id]}
    return Select_table("users", condition)[0]


order_vector = ("Open", "Consc", "Extrav", "Agree", "Neuro")


def dict_to_order_vec(data):
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
    if session.get("logged_in", None):
        scores = calc_from_rawData(data["answers"])

        required_fields = get_fields_table("user_score")
        required_fields["user_id"] = session["user_id"]
        required_fields.update(scores)
        required_fields.pop("id")

        id = Insert_table("user_score", [required_fields])

        if id:
            return make_response(None, True, "Score Posted")
        else:
            return make_response(None, False, "Score not posted")

    return make_response(None, False, "user details not found in the session")


def make_recommendations_data(user_id, compatable_users):
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


def get_user_recommendations():
    user_id = session.get("user_id", None)
    if session.get("logged_in", None) and user_id:
        compatable_users = find_compatible_vectors(user_id)
        final_compatable = make_recommendations_data(
            session["user_id"], compatable_users
        )
        print(final_compatable)
        return make_response(final_compatable, True, f"compatibility recommendations ")
    return make_response(None, False, "user details not found in the session")


def calc_from_rawData(answers):
    answers = list(map(int, answers[:50]))
    print(answers)
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
        print("insert_initial_data")
        data = pd.read_json("src/datasets/data.json")
        l = []
        for i in range(1, len(data) + 1):
            l.append({"mobile": i})
        ids = Insert_table("users", l)
        print(ids)

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
