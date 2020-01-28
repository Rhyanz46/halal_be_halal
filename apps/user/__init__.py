from apps.user.interfaces import bp


class UserModule:
    def __init__(self):
        from apps.user.models import UserDetail
        from apps.user.models import User
        from apps.user.models.addresses import Addresses

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
