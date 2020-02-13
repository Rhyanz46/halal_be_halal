from flask import Blueprint
from apps.order.interface import (
    Order
)


class OrderModule:
    def __init__(self):
        from apps.order.models import Order
        from apps.order.models.currency import Currency
        from apps.order.models.payment import PaymentMethod
        from apps.order.models.cart import Cart, CartItem
        from apps.order.models.package import Package

    @staticmethod
    def init_app(app):
        bp = Blueprint('order', __name__, url_prefix='/order')
        bp.add_url_rule('', view_func=Order.as_view(''))
        app.register_blueprint(bp)
