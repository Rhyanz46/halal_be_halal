from datetime import datetime
from core.database import db


class FoodFeedBack(db.Model):
    __tablename__: str = 'food_feed_back'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    comment = db.Column(db.Text)
    ratting = db.Column(db.SmallInteger)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
