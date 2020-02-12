from datetime import datetime
from core.database import db


class Cart(db.Model):
    # relationship with order
    __tablename__: str = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())


class CartItem(db.Model):
    __tablename__: str = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.TEXT)
    qty = db.Column(db.BigInteger)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    packages = db.relationship('Package', backref='cart', lazy=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())


# user -> order -> cart
# user -> cart -> order
