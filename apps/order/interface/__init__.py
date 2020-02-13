from flask import request
from flask.views import MethodView
from core import parser

from apps.order.services import post_order, my_order_list


class Order(MethodView):
    @staticmethod
    def post():
        data = parser.ValueChecker(request.json)
        data.parse("user_id", int, length=11)
        data.parse("order_time", str, length=11)
        data.parse("order_loc", dict)
        data.parse("deliver_to", dict)
        data.parse("notes", str, length=100)
        data.parse("items", list)
        return post_order(data.get_parsed())

    @staticmethod
    def get():
        page = request.args.get('page')
        if not page:
            page = 1
        return my_order_list(page, per_page=10)
