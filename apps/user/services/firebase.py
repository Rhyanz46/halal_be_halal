from core.config import firebase_app
from firebase_admin.auth import (
    verify_id_token as firebase_verify_id_token,
    InvalidIdTokenError,
)


def firebase_auth_token(token):
    try:
        response = firebase_verify_id_token(token, app=firebase_app, check_revoked=False)
    except InvalidIdTokenError:
        return {"message": "token is not a valid for Firebase ID token"}, 400
    print(response)
    return {"message": "berhasil"}
