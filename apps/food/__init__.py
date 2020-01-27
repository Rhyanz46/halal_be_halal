from flask import Blueprint
from apps.food.interfaces import (
    Foods,
    FoodCategory,
    FoodImages,
    FoodDetail,
    FoodCategoryDetail
)


class FoodModule:
    def __init__(self):
        from apps.food.models.images import FoodImage
        from apps.food.models.history import FoodHistory
        from apps.food.models.certificate import Certificate
        from apps.food.models.certificate_giver import CertificateGiver
        from apps.food.models.theme import FoodTheme
        from apps.food.models.tags import FoodTag
        from apps.food.models.feedback import FoodFeedBack
        from apps.food.models import Food

    @staticmethod
    def init_app(app):
        bp = Blueprint('food', __name__, url_prefix='/food')
        bp.add_url_rule('', view_func=Foods.as_view('wawaw'))
        bp.add_url_rule('/<int:food_id>/images', view_func=FoodImages.as_view('food_images'))
        bp.add_url_rule('/<int:food_id>', view_func=FoodDetail.as_view('food_detail'))
        # bp.add_url_rule('/category', view_func=FoodCategory.as_view('food_category'))
        # bp.add_url_rule('/category/<string:name>', view_func=FoodCategory.as_view('food_category_detail'))
        app.register_blueprint(bp)
