from apps.package.interfaces import bp


class PackageModule:
    def __init__(self):
        from apps.package.models import Package

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
