from apps.user.interfaces import bp


class UserModule:
    def __init__(self):
        from apps.user.models import User
        from apps.user.models.details import UserDetail
        from apps.user.models.addresses import Addresses
        from apps.user.models.social_media import SocialMedia

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
