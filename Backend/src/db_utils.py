from src.models.user_models import *
# from models.processing_models import *

from sqlalchemy import create_engine,insert

# Create an engine for a SQLite database
engine = create_engine('sqlite:///database.db', echo=True)

tables={
    "Users":Users,
    "User_score":User_score
}

def get_fields_table(tbl):
    required_fields=[x.name for x in tables[tbl].__table__.columns ]
    return required_fields

def Insert_table(tbl,data):
    res=engine.execute(insert(tables[tbl]),data)
    return res


def user_login():
    pass

def get_user_mobile(mobile):
    pass
