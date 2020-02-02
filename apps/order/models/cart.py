from datetime import datetime
from core.database import db

food_cart = db.Table('food_cart',
                        db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                        db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True))


class Cart(db.Model):
    __tablename__: str = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.TEXT)
    user_detail_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    foods_ = db.relationship('Food', secondary=food_cart, backref='cart', lazy='subquery')
    packages = db.relationship('Package', backref='cart', lazy=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
