from apps.store.interfaces import bp


class StoreModule:
    def __init__(self):
        from apps.store.models import Store

    @staticmethod
    def init_app(app):
        app.register_blueprint(bp)
