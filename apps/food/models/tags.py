from datetime import datetime
from core.database import db


class FoodTag(db.Model):
    __tablename__: str = 'food_tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
