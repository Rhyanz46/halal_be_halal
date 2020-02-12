from datetime import datetime
from core.database import db


class Addresses(db.Model):
    __tablename__: str = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    latitude = db.Column(db.Float, default=0.0)
    longitude = db.Column(db.Float, default=0.0)
    address = db.Column(db.Text)
    note = db.Column(db.Text)
    accuracy = db.Column(db.Float, default=0.0)

    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
