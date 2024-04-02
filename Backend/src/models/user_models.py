from src.extension import db

class users(db.Model):
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
    

class user_score(db.Model):
    __tablename__ = "user_score"

    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"),primary_key=True)
    Open = db.Column(db.Integer(), nullable=False)
    Consc = db.Column(db.Integer(), nullable=False)
    Extrav = db.Column(db.Integer(), nullable=False)
    Agree = db.Column(db.Integer(), nullable=False)
    Neuro = db.Column(db.Integer(), nullable=False)


    def __repr__(self):
        return f"<user_score {self.user_id}>"
    
