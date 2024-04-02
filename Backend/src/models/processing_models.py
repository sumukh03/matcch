from src.extension import db
import pandas as pd



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
    


# class openness_compatability(db.Model):
#     __tablename__ = "openness_compatability"

#     category = db.Column(db.String(1),primary_key=True)
#     A = db.Column(db.Integer(), nullable=False)
#     B = db.Column(db.Integer(), nullable=False)
#     C = db.Column(db.Integer(), nullable=False)
#     D = db.Column(db.Integer(), nullable=False)
#     E = db.Column(db.Integer(), nullable=False)
#     F = db.Column(db.Integer(), nullable=False)
#     G = db.Column(db.Integer(), nullable=False)
#     H = db.Column(db.Integer(), nullable=False)
#     I = db.Column(db.Integer(), nullable=False)
#     J = db.Column(db.Integer(), nullable=False)


#     def __repr__(self):
#         return f"<openness_compatability {self.category}>"
    


# class conscientiousness_compatability(db.Model):
#     __tablename__ = "conscientiousness_compatability"

#     category = db.Column(db.String(1),primary_key=True)
#     A = db.Column(db.Integer(), nullable=False)
#     B = db.Column(db.Integer(), nullable=False)
#     C = db.Column(db.Integer(), nullable=False)
#     D = db.Column(db.Integer(), nullable=False)
#     E = db.Column(db.Integer(), nullable=False)
#     F = db.Column(db.Integer(), nullable=False)
#     G = db.Column(db.Integer(), nullable=False)
#     H = db.Column(db.Integer(), nullable=False)
#     I = db.Column(db.Integer(), nullable=False)
#     J = db.Column(db.Integer(), nullable=False)


#     def __repr__(self):
#         return f"<conscientiousness_compatability {self.category}>"
    


