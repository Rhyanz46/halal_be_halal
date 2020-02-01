from datetime import date
from flask import Blueprint, request

from core import method_is, parser

from ..services import (
    register,
    login,
    update,
    show_user_detail,
    user_list,
    delete_user,
    get_my_address,
    post_my_address,
    get_my_social_media,
    post_my_social_media
)
from apps.user.services.firebase import firebase_auth_token

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('', methods=['GET'])
def index():
    username = request.args.get('username')
    return show_user_detail(username)


@bp.route('/register', methods=['POST'])
def _register():
    data = parser.ValueChecker(request.json)
    data.parse('username', field_type=str, length=30)
    data.parse('email', field_type=str, length=30)
    data.parse('fullname', field_type=str, length=30)
    data.parse('phone_number', field_type=int, length=30)
    data.parse('password', field_type=str, length=30)
    return register(data.get_parsed())


@bp.route('/auth', methods=['POST'])
def auth():
    data = parser.ValueChecker(request.json)
    data.parse('username', field_type=str, length=30)
    data.parse('password', field_type=str, length=30)
    return login(data.get_parsed())


@bp.route('/auth/firebase-token', methods=['POST'])
def firebase_token_verify():
    data = parser.ValueChecker(request.json)
    data.parse('token', field_type=str, length=3000)
    data = data.get_parsed()
    return firebase_auth_token(data['token'])


@bp.route('/detail/<string:username>', methods=['PUT', 'GET', 'DELETE'])
def do_update(username):
    data = parser.ValueChecker(request.json)
    data.parse('username', field_type=str, nullable=True, length=30)
    data.parse('email', field_type=str, nullable=True, length=30)
    data.parse('fullname', field_type=str, nullable=True, length=30)
    data.parse('address', field_type=str, nullable=True, length=30)
    data.parse('phone_number', field_type=int, nullable=True, length=30)
    data.parse('work_start_time', field_type=date, nullable=True,  length=30)
    data.parse('activate', field_type=bool, nullable=True,  length=30)
    data.parse('password', field_type=str, nullable=True, length=30)

    if method_is('PUT'):
        return update(username, data.get_parsed())
    elif method_is('GET'):
        return show_user_detail(username)
    elif method_is('DELETE'):
        return delete_user(username)
    return {"message": "waw"}, 200


@bp.route('/list', methods=['GET'])
def list_():
    page = request.args.get('page')
    return user_list(page)


@bp.route('/address', methods=['POST', 'GET'])
def address():
    if method_is('GET'):
        return get_my_address()
    data = parser.ValueChecker(request.json)
    data.parse('name', field_type=str, length=30)
    data.parse('latitude', field_type=str, nullable=True, length=30)
    data.parse('longitude', field_type=str, nullable=True, length=30)
    data.parse('address', field_type=str, length=30)
    data.parse('note', field_type=str, nullable=True, length=30)
    return post_my_address(data.get_parsed())


@bp.route('/social-media', methods=['POST', 'GET'])
def social_media():
    if method_is('GET'):
        return get_my_social_media()
    data = parser.ValueChecker(request.json)
    data.parse('uid', field_type=str, length=30)
    data.parse('image', field_type=str, nullable=True, length=30)
    data.parse('provider', field_type=str, nullable=True, length=30)
    data.parse('link', field_type=str, length=30)
    return post_my_social_media(data.get_parsed())
