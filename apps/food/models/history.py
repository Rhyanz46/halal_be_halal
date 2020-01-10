from datetime import datetime
from core.database import db


class FoodHistory(db.Model):
    __tablename__ = 'food_history'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    user_detail_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    action_name = db.Column(db.String(255))
    time_created = db.Column(db.DateTime, default=datetime.now())
