from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from core.config import config


def create_app(test_config=None):
    app = Flask(__name__, static_folder=config['STATIC_FOLDER'])
    if test_config is not None:
        app.config.from_mapping(test_config)
    app.config.from_mapping(config)

    from core.cli import CLI
    from core.database import db

    from apps.user import UserModule
    from apps.food import FoodModule
    from apps.store import StoreModule
    from apps.order import OrderModule
    from apps.package import PackageModule
    from apps.driver import DriverModule
    # from apps.category_access import CategoryAccessModule

    cli = CLI()
    cors = CORS()
    migrate = Migrate()
    jwt = JWTManager(app)

    user = UserModule()
    food = FoodModule()
    store = StoreModule()
    order = OrderModule()
    package = PackageModule()
    driver = DriverModule()
    # category_access = CategoryAccessModule()

    jwt.init_app(app)
    cli.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    user.init_app(app)
    food.init_app(app)
    store.init_app(app)
    order.init_app(app)
    package.init_app(app)
    driver.init_app(app)
    # category_access.init_app(app)

    return app
