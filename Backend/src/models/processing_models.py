from src.extension import db
import pandas as pd


class user_score(db.Model):
    __tablename__ = "user_score"

    user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"), primary_key=True)
    Open = db.Column(db.Integer(), nullable=False)
    Consc = db.Column(db.Integer(), nullable=False)
    Extrav = db.Column(db.Integer(), nullable=False)
    Agree = db.Column(db.Integer(), nullable=False)
    Neuro = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"<user_score {self.user_id}>"


class compatibility(db.Model):
    __tablename__ = "compatibility"

    id = db.Column(db.Integer(), primary_key=True)
    user_id1 = db.Column(db.Integer(), db.ForeignKey("users.user_id"), nullable=False)
    user_id2 = db.Column(db.Integer(), db.ForeignKey("users.user_id"), nullable=False)
    Open = db.Column(db.Integer(), nullable=False)
    Consc = db.Column(db.Integer(), nullable=False)
    Extrav = db.Column(db.Integer(), nullable=False)
    Agree = db.Column(db.Integer(), nullable=False)
    Neuro = db.Column(db.Integer(), nullable=False)
    total = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"<compatibility {self.user_id}>"
