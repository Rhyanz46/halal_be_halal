from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..models import User, UserDetail
# from apps.category_access.models import CategoryAccess
from datetime import timedelta

from .list import user_list

expires = timedelta(days=1)


def full_edit_user(data, user_target):
    username_exist = User.query.filter_by(username=data['username']).first()
    email_exist = User.query.filter_by(email=data['email']).first()
    phone_exist = UserDetail.query.filter_by(phone_number=data['phone_number']).first()
    if username_exist:
        return {'message': 'username is exist'}, 400
    elif email_exist:
        return {'message': 'email is exist'}, 400
    elif phone_exist:
        return {'message': 'phone_number is already used'}, 400

    if data['username'] != None:
        user_target.username = data['username']
    if data['email'] != None:
        user_target.email = data['email']
    if data['fullname'] != None:
        user_target.fullname = data['fullname']
    if data['address'] != None:
        user_target.address = data['address']
    if data['phone_number'] != None:
        user_target.phone_number = data['phone_number']
    if data['work_start_time'] != None:
        user_target.work_start_time = data['work_start_time']
    if data['activate'] != None:
        user_target.activate = data['activate']
    if data['password'] != None:
        user_target.password = data['password']
    return user_target


def store_data_user(data):
    detail = UserDetail(
        fullname=data['fullname'],
        phone_number=data['phone_number'],
    )

    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        user_detail=detail
    )
    # try:
    user.commit()
    return user
    # except:
    #     return None


def register(data):
    username_exist = User.query.filter_by(username=data['username']).first()
    email_exist = User.query.filter_by(email=data['email']).first()
    phone_exist = UserDetail.query.filter_by(phone_number=data['phone_number']).first()

    # user = User.query.filter_by(id=get_jwt_identity()).first()
    # if not user:
    #     return {"message": "user authentication is wrong"}, 400

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    # if not ca.root_access:
    #     return {"message": "you have not access"}, 403

    if username_exist:
        return {'message': 'username is exist'}, 400
    elif email_exist:
        return {'message': 'email is exist'}, 400
    elif phone_exist:
        return {'message': 'phone_number is already used'}, 400

    saved = store_data_user(data)
    if not saved:
        return {'error': 'failed to save data'},
    token = create_access_token(identity=saved.id, expires_delta=expires)
    return {'token': token}


def login(data):
    username = data['username']
    password = data['password']
    user = User.query.filter(User.username == username, User.password == password).first()
    if user:
        # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
        # ca_name = None
        # if ca:
        # ca_name = ca.name
        token = create_access_token(identity=user.id, expires_delta=expires)
        return {'token': token}, 200
    return {'data': 'username atau password salah'}, 403


@jwt_required
def update(username, data):
    user_target = User.query.filter_by(username=username).first()

    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user authentication is wrong"}, 400

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    if not user_target:
        return {'error': 'user is not found'}, 402

    if user.id == user_target.id:
        user_target = full_edit_user(data, user_target)
    else:
        # if not ca.root_access:
        if data['username'] != None:
            return {'error': 'you have not permission to edit username of this user'}, 403
        if data['email'] != None:
            return {'error': 'you have not permission to edit email of this user'}, 403
        if data['fullname'] != None:
            return {'error': 'you have not permission to edit fullname of this user'}, 403
        if data['address'] != None:
            return {'error': 'you have not permission to edit address of this user'}, 403
        if data['phone_number'] != None:
            return {'error': 'you have not permission to edit phone number of this user'}, 403
        if data['work_start_time'] != None:
            user_target.work_start_time = data['work_start_time']
        if data['activate'] != None:
            user_target.activate = data['activate']
        if data['password'] != None:
            return {'error': 'you have not permission to password of this user'}, 403
        # else:
        #     user_target = full_edit_user(data, user_target)
    try:
        user_target.commit()
    except:
        return {'error': 'something wrong'}, 402
    return {'message': "update"}, 200


@jwt_required
def show_user_detail(username=None):
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user authentication is wrong"}, 400

    if not isinstance(None, type(username)):
        user_target = User.query.filter_by(username=username).first()
    else:
        user_target = user

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    if not user_target:
        return {'error': 'user is not found'}, 402

    if user.id == user_target.id:
        return user_target.__serialize__(detail=True), 200

    # if not ca.show_user:
    #     return {"message": "you not have permission"}, 403

    return user_target.__serialize__(detail=True), 200


@jwt_required
def delete_user(username):
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user authentication is wrong"}, 400

    if not isinstance(None, type(username)):
        user_target = User.query.filter_by(username=username).first()
    else:
        user_target = user

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    if not user_target:
        return {'error': 'user is not found'}, 402

    # if not ca.root_access:
    #     return {"message": "this action only for root access"}, 403

    try:
        user_target.delete()
    except:
        return {'error': 'kesalahan saat menghapus, tanyakan masalah ini ke backend'}, 500
    return {'message': 'berhasil menghapus {}'.format(username)}
