from datetime import datetime
from core.database import db


class Addresses(db.Model):
    __tablename__: str = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    address = db.Column(db.Text)
    note = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
