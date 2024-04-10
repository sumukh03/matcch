from src.extension import db
from flask_login import UserMixin


class users(db.Model, UserMixin):
    __tablename__ = "users"

    user_id = db.Column(db.Integer(), primary_key=True)
    mobile = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<users {self.user_id}>"
