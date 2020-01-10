from apps.user.interfaces import bp


class UserModule:
    def __init__(self):
        from apps.user.models import UserDetail
        from apps.user.models import User

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
