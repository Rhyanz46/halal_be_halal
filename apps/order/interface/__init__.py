from flask import request
from flask.views import MethodView
from core import parser

from apps.order.services.cart import post_cart


class Cart(MethodView):
    @staticmethod
    def post():
        data = parser.ValueChecker(request.json)
        data.parse("food_id", int, length=11)
        data.parse('amount', int, nullable=True, length=11)
        return post_cart(data.get_parsed())
