from src.extension import db
from flask_login import UserMixin

class users(db.Model,UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(20),unique=True,nullable=False)
    city = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(8), nullable=False)


    def __repr__(self):
        return f"<users {self.user_id}>"
    


    
