from core.database import db
from datetime import datetime


class Order(db.Model):
    __tablename__: str = 'order'
    id = db.Column(db.Integer, primary_key=True)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    total = db.Column(db.Float, default=0.0)
    paid = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(30), default="In Progress")
    notes = db.Column(db.Text)
    user_detail_id = db.Column(db.Integer, db.ForeignKey('user_detail.id'))

    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    order_time = db.Column(db.DateTime, default=datetime.now())
    cart = db.relationship('Cart', uselist=False, backref='order')
    order_loc = db.relationship('OrderLocationTracked', uselist=False, backref='order_loc')
    deliver_to = db.relationship('OrderLocationTracked', uselist=False, backref='deliver_to')
    created_timestamp = db.Column(db.DateTime, default=datetime.now())

    def get(self):
        carts = []
        for cart in self.cart.cart_items:
            carts.append({
              "item": cart.food.name,
              "count": cart.qty,
              "note": cart.note
            })
        data = {
          "id": self.id,
          "orders": carts,
          "payment": self.payment_method_id,
          "total": self.total,
          "paid": self.paid,
          "state": self.state,
          "driver": "belum ada driver"
        }
        if self.driver:
            drv = {
                "id": self.driver,
                "name": self.driver.user_detail.fullname,
                "image": self.driver.user_detail.image,
                "phone": self.driver.user_detail.phone_number,
                "rating": self.driver.ratting
            }
            data.update({"driver": drv})
        return data


class OrderLocationTracked(db.Model):
    __tablename__: str = 'order_location_tracked'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, default=0.0)
    longitude = db.Column(db.Float, default=0.0)
    accuracy = db.Column(db.Float, default=0.0)
    is_pinned = db.Column(db.Boolean, default=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
