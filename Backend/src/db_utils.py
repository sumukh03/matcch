from src.models.user_models import *
# from models.processing_models import *
from src.extension import db
from sqlalchemy import create_engine,insert,select,and_
from sqlalchemy.orm import sessionmaker

# Create an engine for a SQLite database
engine = create_engine('sqlite:///instance/database.db', echo=True)



tables={
    "users":users,
    "user_score":user_score
}

def get_fields_table(tbl):
    required_fields={x.name:"" for x in tables[tbl].__table__.columns }
    return required_fields

def Insert_table(tbl,data):

    result = engine.execute(
        insert(tables[tbl]),data,
    )
    # res=engine.execute(insert(tables[tbl]).values(**data)).commit()
    return result


def Select_table(tbl,condition):
    # condition={column:["mobile"],value:["960..."]}
    filter_conditions = [
        getattr(tables[tbl],k)==v for k,v in zip(condition["column"],condition["value"])
    ]

    output=[]

    result = tables[tbl].query.filter(and_(*filter_conditions)).all()
    #output i.e , the result is the object representation of the model 
    for row in result: # filtering the _sa_instance_state that is associated with the model , and retrieveing values
        keys=row.__dict__
        keys.pop('_sa_instance_state',None)
        output.append(keys)


    return output

    
