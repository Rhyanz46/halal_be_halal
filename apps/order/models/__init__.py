from core.database import db
from datetime import datetime


cart_orders = db.Table('cart_orders',
                       db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
                       db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True))


class Order(db.Model):
    __tablename__: str = 'order'
    id = db.Column(db.Integer, primary_key=True)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    total = db.Column(db.Float, default=0.0)
    paid = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(30), default="In Progress")

    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    carts = db.relationship('Cart', secondary=cart_orders, lazy='subquery', backref='order')
    created_timestamp = db.Column(db.DateTime, default=datetime.now())

    def get(self):
        carts = []
        for cart in self.carts:
            cart.append({
              "item": "{food object}",
              "count": 2,
              "note": "note for item"
            })
        data = {
          "id": self.id,
          "orders": carts,
          "payment": self.payment_method,
          "total": self.total,
          "paid": self.paid,
          "state": self.state,
          "driver": {
            "id": self.driver.id,
            "name": self.driver.user_detail.fullname,
            "image": self.driver.user_detail.image,
            "phone": self.driver.user_detail.phone_number,
            "rating": self.driver.ratting
          }
        }
        return data
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
