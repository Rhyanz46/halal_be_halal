from core.database import db
from datetime import datetime


food_orders = db.Table('food_orders',
                       db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True),
                       db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True))


class Order(db.Model):
    __tablename__: str = 'order'
    id = db.Column(db.Integer, primary_key=True)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    total = db.Column(db.Float, default=0.0)
    paid = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(30), default="In Progress")

    foods = db.relationship('Food', secondary=food_orders, lazy='subquery', backref='order')
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
    #
    # data = {
    #     "id": "12345asd312",
    #     "orders": [
    #         {
    #             "item": "{food object}",
    #             "count": 2,
    #             "note": "note for item"
    #         },
    #         {}
    #     ],
    #     "payment": "COD",
    #     "total": 124566,
    #     "paid": False,
    #     "state": "In progress",
    #     "driver": {
    #         "id": 12345,
    #         "name": "abdul",
    #         "image": "http:///dadasdasd.jpg",
    #         "phone": "097983478238",
    #         "rating": 8
    #     }
    # }
