from datetime import datetime
from core.database import db


class Cart(db.Model):
    __tablename__: str = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.TEXT)
    foods = db.relationship('Food', lazy='subquery', backref='order')
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
