from datetime import datetime
from core.database import db

food_cart_items = db.Table('food_cart_items',
                        db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                        db.Column('cart_item_id', db.Integer, db.ForeignKey('cart_item.id'), primary_key=True))


class Cart(db.Model):
    __tablename__: str = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_detail_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())


class CartItem(db.Model):
    __tablename__: str = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.TEXT)
    amount = db.Column(db.BigInteger)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    foods = db.relationship('Food', secondary=food_cart_items, backref='cart_item', lazy='subquery')
    packages = db.relationship('Package', backref='cart', lazy=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())