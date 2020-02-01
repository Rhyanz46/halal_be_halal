from datetime import datetime
from core.database import db


class Driver(db.Model):
    __tablename__: str = 'driver'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    ratting = db.Column(db.Integer, default=0)
    id_card_img = db.Column(db.Text)
    no_id_card = db.Column(db.Text)
    user_detail = db.relationship('UserDetail', uselist=False, backref='driver')
    orders = db.relationship('Order', lazy='subquery', backref='driver')
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
