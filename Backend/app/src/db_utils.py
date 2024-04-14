from src.models.user_models import *
from src.models.processing_models import *
from src.extension import db
from sqlalchemy import create_engine, insert, select, and_, delete, or_, MetaData
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine("sqlite:///instance/database.db", echo=True, pool_pre_ping=True)

tables = {"users": users, "user_score": user_score}


def get_fields_table(tbl):
    required_fields = {x.name: "" for x in tables[tbl].__table__.columns}
    return required_fields


def Insert_table(tbl, data):
    try:
        with engine.connect() as conn:
            result = conn.execute(insert(tables[tbl]), data)
            conn.commit()
        return result
    except Exception as e:
        return False


def Select_table(tbl, condition):
    filter_conditions = [
        getattr(tables[tbl], k) == v
        for k, v in zip(condition["column"], condition["value"])
    ]

    output = []

    result = tables[tbl].query.filter(and_(*filter_conditions)).all()
    for row in result:
        keys = row.__dict__
        keys.pop("_sa_instance_state", None)
        output.append(keys)

    return output


def Delete_table(tbl, condition):
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
    data.to_sql("user_score", con=engine, if_exists="append", index=False)
