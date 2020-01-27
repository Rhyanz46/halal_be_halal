import os
from os.path import join
from dotenv import load_dotenv


import firebase_admin
from firebase_admin import credentials
from os import getcwd


dotenv_path = join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

STATIC_FOLDER = 'static'

DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")


firebase_credential_file = getcwd() + str('/credentials/halalbeehalal-firebase-adminsdk-r8nxj-4de9d7a329.json')
firebase_credential = credentials.Certificate(firebase_credential_file)
firebase_app = firebase_admin.initialize_app(firebase_credential)


config = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_HOST,
        DATABASE_PORT,
        DATABASE_NAME
    ),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': 'keren',
    'APPLICATION_ROOT': os.getcwd(),
    'STATIC_FOLDER': STATIC_FOLDER
}
