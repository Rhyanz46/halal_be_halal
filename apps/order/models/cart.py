from datetime import datetime
from core.database import db


class Cart(db.Model):
    __tablename__: str = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.TEXT)
    user_detail_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
