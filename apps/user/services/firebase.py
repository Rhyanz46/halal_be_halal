from datetime import timedelta
from core.config import firebase_app
from core import random_string
from firebase_admin.auth import (
    verify_id_token as firebase_verify_id_token,
    InvalidIdTokenError
)
from apps.user.services import register
from flask_jwt_extended import create_access_token


def firebase_auth_token(token):
    try:
        response = firebase_verify_id_token(token, app=firebase_app, check_revoked=False)
        username = response['firebase']['identities']['phone'][0].replace('+62', '0')
        password = random_string(10)
    except InvalidIdTokenError:
        return {"message": "token is not a valid for Firebase ID token"}, 400
    data = {
        "fullname": username,
        "address": None,
        "phone_number": username,
        "username": username,
        "email": None,
        "password": password
    }
    return register(data)
