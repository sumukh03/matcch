""" This file acts as a database layer 
    The functions take the data which is mapped to the models(tables) of the application
    sqlalchemy generates required queries"""

from src.models.user_models import *
from src.models.processing_models import *
from src.extension import db
from sqlalchemy import create_engine, insert, select, and_, delete, or_, MetaData
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine("sqlite:///instance/database.db", echo=True, pool_pre_ping=True)

tables = {"users": users, "user_score": user_score}


def get_fields_table(tbl):
    """ Function to get the columns of the table
        It uses the special methods provided by the models
        RETURNS the dictionary {"column_name":""} """
    required_fields = {x.name: "" for x in tables[tbl].__table__.columns}
    return required_fields


def Insert_table(tbl, data):
    """ Function that simulates the SQL INSERT statement
        Accepts the table name and the data as a list of dictionaries that are added to the database
         
        Here, the  """
    try:
        with engine.connect() as conn:
            result = conn.execute(insert(tables[tbl]), data)
            conn.commit()
        return result
    except Exception as e:
        return False


def Select_table(tbl, condition):
    """ This function simulates the SQL SELECT statement
        ACCEPTS the table name and the condition as condition = {"column": ["column_names"], "value": [values]]}
        RETURNS the selected rows as a list
        
        Here we use the getattr() to get the attributes of the table.
        The filter condition is applied on the columns with AND operator
        Note : this simulates only the statement "select () from table_name where condition1 and condition2 ..." """
    
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
