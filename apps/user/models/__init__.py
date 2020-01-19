from datetime import datetime
from core.database import db

from .details import UserDetail


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # category_access_id = db.Column(db.Integer, db.ForeignKey("category_access.id"))
    username = db.Column(db.String(90), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    user_detail = db.relationship('UserDetail', uselist=False, backref='user')
    food_feed_backs = db.relationship('FoodFeedBack', backref='user', lazy=True)
    created_time = db.Column(db.DateTime, default=datetime.now())

    def __serialize__(self, detail=False):
        data = {
            "id": self.id,
            # "category_access_id": self.category_access_id,
            "username": self.username,
            "email": self.email
        }
        if detail:
            data.update({"user_detail": UserDetail().__serialize__(id=self.id)})
        return data
