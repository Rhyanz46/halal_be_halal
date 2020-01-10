from flask_jwt_extended import jwt_required
from ..models import CategoryAccess
from apps.user.models import User
from apps.food.models import user_foods, Food


@jwt_required
def set_ca(data):
    name_exist = CategoryAccess.query.filter_by(name=data['name']).first()
    if name_exist:
        return {"message": "akses bernama {} sudah ada sebelumnya".format(data['name'])}, 400
    access_exist = CategoryAccess.query.filter(
        CategoryAccess.add_user == data['add_user'],
        CategoryAccess.delete_user == data['delete_user'],
        CategoryAccess.edit_user == data['edit_user'],
        CategoryAccess.add_job == data['add_job'],
        CategoryAccess.delete_job == data['delete_job'],
        CategoryAccess.update_job == data['update_job'],
        CategoryAccess.show_job == data['show_job'],
        CategoryAccess.print_job == data['print_job'],
        CategoryAccess.check_job == data['check_job'],
        CategoryAccess.service_job == data['service_job']
    ).first()
    if access_exist:
        return {"message": "kategori seperti ini sudah ada di {}".format(access_exist.name)}, 400
    category_access = CategoryAccess(
        name=data['name'],
        add_user=data['add_user'],
        delete_user=data['delete_user'],
        edit_user=data['edit_user'],
        add_job=data['add_job'],
        delete_job=data['delete_job'],
        update_job=data['update_job'],
        show_job=data['show_job'],
        print_job=data['print_job'],
        check_job=data['check_job'],
        service_job=data['service_job']
    )
    try:
        category_access.commit()
    except:
        return {"message": "error to save {}".format(data['name'])}, 400
    return {"message": "sukses menambah kategori {}".format(data['name'])}


@jwt_required
def get_list_ca(id=None):
    if isinstance(None, type(id)):
        ca = CategoryAccess.query.all()
        result = []
        for a in ca:
            result.append(a.__serialize__())
        if len(result) <= 0:
            return {"data": "empty"}, 204
        return {"data": result}
    ca = CategoryAccess.query.filter_by(id=id).first()
    if not ca:
        return {"data": "category access with id {} is not found".format(id)}, 400
    return {"data": ca.__serialize__()}


@jwt_required
def edit_ca(id, data):
    ca = CategoryAccess.query.filter_by(id=id).first()
    if not ca:
        return {"message": "id {} is not found".format(id)}, 204
    if data['name'] != None:
        ca.name = data['name']
    if data['add_user'] != None:
        ca.add_user = data['add_user']
    if data['delete_user'] != None:
        ca.delete_user = data['delete_user']
    if data['edit_user'] != None:
        ca.edit_user = data['edit_user']
    if data['add_job'] != None:
        ca.add_job = data['add_job']
    if data['delete_job'] != None:
        ca.delete_job = data['delete_job']
    if data['update_job'] != None:
        ca.update_job = data['update_job']
    if data['show_job'] != None:
        ca.show_job = data['show_job']
    if data['print_job'] != None:
        ca.print_job = data['print_job']
    if data['check_job'] != None:
        ca.check_job = data['check_job']
    if data['service_job'] != None:
        ca.service_job = data['service_job']
    try:
        ca.commit()
    except:
        return {"message": "cant save"}, 500
    return {"message": "{} has been updated".format(ca.name)}


@jwt_required
def set_user(ca_id, username, data):
    action = data['action']
    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "user {} is not found".format(username)}, 400

    ca = CategoryAccess.query.filter_by(id=ca_id).first()
    if not ca:
        return {"message": "id {} is not found".format(ca_id)}, 400
    if action == "on":
        try:
            ca.users.append(user)
            ca.commit()
        except:
            return {"message": "error to set {} to {}".format(user.username, ca.name)}, 500
        return {"message": "success to set {} to {}".format(user.username, ca.name)}
    elif action == "off":
        try:
            ca.users.remove(user)
            ca.commit()
        except:
            return {"message": "error to unset {} from {}".format(user.username, ca_id)}, 500
        return {"message": "success to unset {} from {}".format(user.username, ca_id)}


@jwt_required
def users_of_ca(ca_id, page):
    if not page:
        page = 1
    try:
        page = int(page)
    except:
        return {"message": "page param must be integer"}, 400

    ca = CategoryAccess.query.filter_by(id=ca_id).first()
    if not ca:
        return {"message": "this category permission is not found"}, 400
    users = User.query.filter_by(category_access_id=ca_id).paginate(page=page, per_page=1)

    if not users.total:
        return {"message": "no user found at this category permission"}, 400

    result = []
    for item in users.items:
        result.append({"user_id": item.id, "username": item.username})

    meta = {
        "total_data": users.total,
        "total_pages": users.pages,
        "total_data_per_page": users.per_page,
        "next": "?page={}".format(users.next_num) if users.has_next else None,
        "prev": "?page={}".format(users.prev_num) if users.has_prev else None
    }
    return {"data": result, "meta": meta}
