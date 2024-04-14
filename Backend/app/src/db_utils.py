from src.models.user_models import *
from src.models.processing_models import *
from src.extension import db
from sqlalchemy import create_engine, insert, select, and_, delete, or_
from sqlalchemy.orm import sessionmaker
import os
# Create an engine for a SQLite database
engine = create_engine("sqlite:///instance/database.db", echo=True)

# URL=os.environ["DB_URL"]
# engine = create_engine(
#     "postgresql://postgres:postgres@db:3307/postgres"
#    )
# engine = create_engine(
#     os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:root@db:3306/matcch'))
# engine = create_engine(
#     "mysql+pymysql://root:root@mysql:3307/matcch")

# engine = create_engine(f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['MYSQL_HOST']}/{os.environ['MYSQL_DATABASE']}")
# DATABASE_URI = os.environ.get('DATABASE_URI')

# engine = create_engine("mysql+pymysql://username:password@db:3306/dbname")

tables = {"users": users, "user_score": user_score}


def get_fields_table(tbl):
    required_fields = {x.name: "" for x in tables[tbl].__table__.columns}
    return required_fields


def Insert_table(tbl, data):

    # result = engine.execute(
    #     insert(tables[tbl]),
    #     data,
    # )


    with engine.connect() as conn:
        result=conn.execute(insert(tables[tbl]),
        data)
        
    return result


def Select_table(tbl, condition):
    # condition={column:["mobile"],value:["960..."]}
    filter_conditions = [
        getattr(tables[tbl], k) == v
        for k, v in zip(condition["column"], condition["value"])
    ]

    output = []

    result = tables[tbl].query.filter(and_(*filter_conditions)).all()
    # output i.e , the result is the object representation of the model
    for (
        row
    ) in (
        result
    ):  # filtering the _sa_instance_state that is associated with the model , and retrieveing values
        keys = row.__dict__
        keys.pop("_sa_instance_state", None)
        output.append(keys)

    return output


def Delete_table(tbl, condition):
    # delete(user_table).where(user_table.c.name == "patrick")
    # condition = {"column":["col_name"],"value":["value"]}
    filter_conditions = [
        getattr(tables[tbl], k) == v
        for k, v in zip(condition["column"], condition["value"])
    ]

    stmt = delete(tables[tbl]).where(or_(*filter_conditions))
    result = engine.execute(stmt)
    if result:
        return True
    return False


def Insert_df(data):
    print("Insert_df")
    data.reset_index(inplace=True)
    data.rename(columns={"index": "user_id"}, inplace=True)
    data.user_id += 1
    data.to_sql("user_score", con=engine.connect(), if_exists="append", index=False)
