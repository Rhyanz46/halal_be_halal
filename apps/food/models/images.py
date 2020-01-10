from datetime import datetime
from core.database import db


class FoodImage(db.Model):
    __tablename__ = 'food_image'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    link = db.Column(db.String(255))
    main = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime, default=datetime.now())
