from flask import Blueprint

bp = Blueprint('driver', __name__, url_prefix='/driver')


@bp.route('/')
def index():
    return "waw"