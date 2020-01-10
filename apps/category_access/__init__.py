from apps.category_access.interfaces import bp


class CategoryAccessModule:
    def __init__(self):
        from apps.category_access.models import CategoryAccess

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
