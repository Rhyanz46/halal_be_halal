from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import Store


@jwt_required
def create_store(data):
    store = Store.query.filter_by(owner=get_jwt_identity()).first()
    if store:
        return {"message": "you already have a store"}, 400
    name_exist = Store.query.filter_by(name=data['name']).first()
    if name_exist:
        return {"error": "store with `{}` is exist".format(data['name'])}, 400
    store = Store(
        name=data['name'],
        description=data['description'],
        lat=data['lat'],
        lang=data['lang'],
        owner=get_jwt_identity()
    )
    try:
        store.commit()
    except:
        return {"error": "error to save, tell your backend"}, 500
    return {"message": "success to create {} store".format(store.name)}


@jwt_required
def my_store():
    store = Store.query.filter_by(owner=get_jwt_identity()).first()
    if store:
        return store.__serialize__()
    return {"message": "you have no store"}, 400
