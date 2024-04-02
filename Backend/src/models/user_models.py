from src import db

class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(20), primary_key=True)
    city = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(8), nullable=False)


    def __repr__(self):
        return f"<user_data {self.user_id}>"
    

class User_score(db.Model):
    __tablename__ = "User_score"

    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Open = db.Column(db.Integer(), nullable=False)
    Consc = db.Column(db.Integer(), nullable=False)
    Extrav = db.Column(db.Integer(), nullable=False)
    Agree = db.Column(db.Integer(), nullable=False)
    Neuro = db.Column(db.Integer(), nullable=False)


    def __repr__(self):
        return f"<user_data {self.user_id}>"
    
