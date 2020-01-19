from flask import Blueprint, request
from core import method_is, parser

bp = Blueprint('package', __name__, url_prefix='/package')


@bp.route('', methods=['POST', 'GET'])
def index():
    if method_is("POST"):
        data = parser.ValueChecker(request.json)
        data.parse('name', str, length=90)
        data.parse('description', str, length=300)
        data.parse('lat', float, length=15)
        data.parse('lang', float, length=15)
        # return create_store(data.get_parsed())
