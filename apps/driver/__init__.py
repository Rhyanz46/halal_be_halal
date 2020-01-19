from apps.driver.interfaces import bp


class DriverModule:
    def __init__(self):
        from apps.driver.models import Driver

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
