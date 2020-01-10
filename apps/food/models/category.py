from datetime import datetime
from core.database import db


class FoodCategory(db.Model):
    __tablename__ = 'food_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    foods = db.relationship('Food', lazy='subquery', backref='food_category')
    time_created = db.Column(db.DateTime, default=datetime.now())
