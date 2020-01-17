import os
from os.path import join
from dotenv import load_dotenv

dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

STATIC_FOLDER = 'static'

DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

config = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://{}:{}@{}:3307/{}'.format(
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_HOST,
        DATABASE_NAME
    ),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': 'keren',
    'APPLICATION_ROOT': os.getcwd(),
    'STATIC_FOLDER': STATIC_FOLDER
}
