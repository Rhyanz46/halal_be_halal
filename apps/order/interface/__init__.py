from flask import Blueprint, request
from core import method_is, parser

bp = Blueprint('payment', __name__, url_prefix='/payment')


@bp.route('', methods=['POST', 'GET'])
def payment():
    if method_is('POST'):
        data = parser.ValueChecker(request.json)
        data.parse('name', field_type=str, length=50)
        # return set_ca(data.get_parsed())
