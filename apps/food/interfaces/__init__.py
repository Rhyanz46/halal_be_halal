from datetime import date
from flask import Blueprint, request
from core import parser
from flask.views import MethodView

from apps.food.services import (
    create_food,
    my_food_list,
    detail_food,
    food_category,
    food_category_list,
    users_of_food,
    upload_food_image,
    images_of_food
)

bp = Blueprint('fooddawed', __name__, url_prefix='/fodwaeod')


class Foods(MethodView):
    @staticmethod
    def get():
        return my_food_list(request.args.get('page'))

    @staticmethod
    def post():
        data = parser.ValueChecker(request.json)
        data.parse('name', str, length=100)
        data.parse('description', str, nullable=True, length=300)
        data.parse('price', float, length=100)
        data.parse('discount', float, nullable=True, length=100)
        data.parse('category_id', int, length=11)
        data.parse('users', list, nullable=True)
        data.parse('stock', int)
        return create_food(data.get_parsed())


class FoodImages(MethodView):
    @staticmethod
    def post(food_id):
        data = parser.ValueChecker(request.json)
        data.parse('image', str)
        data.parse('main', bool, nullable=True)
        return upload_food_image(food_id, data.get_parsed())

    @staticmethod
    def get(food_id):
        return images_of_food(food_id)


class FoodDetail(MethodView):
    @staticmethod
    def get(food_id):
        return detail_food(food_id)

    @staticmethod
    def delete(food_id):
        return detail_food(food_id, mode='delete')

    @staticmethod
    def put(food_id):
        data = parser.ValueChecker(request.json)
        data.parse('name', str, nullable=True, length=100)
        data.parse('description', str, nullable=True, length=300)
        data.parse('start_time', date, nullable=True, length=100)
        data.parse('deadline', date, nullable=True, length=100)
        data.parse('done', bool, nullable=True, length=100)
        return detail_food(food_id, data.get_parsed(), mode='edit')


class FoodCategory(MethodView):
    @staticmethod
    def get():
        return food_category_list(request.args.get('page'))

    @staticmethod
    def post():
        data = parser.ValueChecker(request.json)
        data.parse('name', str, length=200)
        return food_category(data.get_parsed()['name'])


class FoodCategoryDetail(MethodView):
    @staticmethod
    def delete(name):
        return food_category(name, mode='delete')


@bp.route('/<int:job_id>/users', methods=['PUT', 'GET', 'DELETE'])
def food_users(job_id):
    return users_of_food(job_id)
