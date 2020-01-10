from flask import Blueprint, request
from core import method_is, parser

from ..services import (
    create_store,
    my_store
)

bp = Blueprint('store', __name__, url_prefix='/store')


@bp.route('', methods=['POST', 'GET'])
def index():
    if method_is("GET"):
        return my_store()
    data = parser.ValueChecker(request.json)
    data.parse('name', str, length=90)
    data.parse('description', str, length=300)
    data.parse('lat', float, length=15)
    data.parse('lang', float, length=15)
    return create_store(data.get_parsed())
