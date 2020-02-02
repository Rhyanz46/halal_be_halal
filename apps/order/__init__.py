from apps.order.interface import bp


class OrderModule:
    def __init__(self):
        from apps.order.models import Order
        from apps.order.models.currency import Currency
        from apps.order.models.payment import PaymentMethod
        from apps.order.models.cart import Cart
        from apps.order.models.package import Package

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
