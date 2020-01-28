from flask_jwt_extended import get_jwt_identity, jwt_required
from apps.food.models import Food, user_foods
from apps.food.models.category import FoodCategory
from apps.food.models.images import FoodImage
from apps.user.models import User
from apps.store.models import Store
from core import base64_to_png
from core.config import STATIC_FOLDER
# from apps.category_access.models import CategoryAccess

from flask import current_app, request


@jwt_required
def create_food(data):
    food_ca_ = FoodCategory.query.filter_by(id=data['category_id']).first()
    if not food_ca_:
        return {"error": "category id is not found"}, 400

    store = Store.query.filter_by(owner=get_jwt_identity()).first()
    if not store:
        return {"error": "you have to create store first"}, 403

    # likes = data['like']
    # images = data['image']

    food = Food(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        discount=data['discount'],
        category_id=data['category_id'],
        stock=data['stock']
    )
    store.foods.append(food)

    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user authentication is wrong"}, 400

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    # if not ca.add_food:
    #     return {"message": "you not have permission"}, 403

    food.commit()
    store.commit()

    try:
        food.commit()
    except:
        return {"message": "failed to save food, tell you backend"}, 500
    return {"message": "success to create {} food".format(food.name)}


@jwt_required
def images_of_food(food_id):
    food = Food.query.filter_by(id=food_id).first()
    if not food:
        return {"error": "food is not found"}, 400
    images = []
    for item in food.images:
        link = request.host_url + STATIC_FOLDER + '/' + item.link
        data = {
            "id": item.id,
            "link": link,
            "main": item.main
        }
        images.append(data)
    return {"data": images}


@jwt_required
def upload_food_image(food_id, data):
    folder = current_app.config['APPLICATION_ROOT'] + '/' + STATIC_FOLDER + '/'
    food = Food.query.filter_by(id=food_id).first()
    store = Store.query.filter_by(owner=get_jwt_identity()).first()
    if not store:
        return {"error": "you have to create store first"}, 403
    if not food:
        return {"error": "food is not found"}, 400
    if len(food.images) >= 5:
        return {"error": "max 5 image"}, 400
    if data['image']:
        name = base64_to_png(data['image'], image_path=folder)
        if not name:
            return {"error": "wrong file"}, 400
        if data['main']:
            for chnge_img in food.images:
                chnge_img.main = False
                try:
                    chnge_img.commit()
                except:
                    return {"error": "error 01:10:17:41, tell you backend!!"}, 500
        else:
            data['main'] = False
        image = FoodImage(
            link=name,
            main=data['main']
        )
        food.images.append(image)
        try:
            food.commit()
        except:
            return {"error": "error to add"}, 500
        return {"message": "success"}
    return {"error": "you have to set a file"}, 400


@jwt_required
def my_food_list(page):
    if not page:
        page = 1
    try:
        page = int(page)
    except:
        return {"error": "parameter page must be integer"}, 400
    store = Store.query.filter_by(owner=get_jwt_identity()).first()
    if not store:
        return {"error": "you have to create store first"}, 403

    user = User.query.filter_by(id=get_jwt_identity()).first()
    foods = Food.query. \
        join(Store).filter(
            Store.owner == user.id
        ).paginate(per_page=20, page=page)

    if not foods.total:
        return {"message": "you have not foods"}, 204

    my_foods = []

    for item in foods.items:
        my_foods.append(item.__serialize__(with_img=True))

    meta = {
        "total_data": foods.total,
        "total_pages": foods.pages,
        "total_data_per_page": foods.per_page,
        "next": "?page={}".format(foods.next_num) if foods.has_next else None,
        "prev": "?page={}".format(foods.prev_num) if foods.has_prev else None
    }
    return {"data": my_foods, "meta": meta}


@jwt_required
def detail_food(food_id, data=None, mode=None):
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user authentication is wrong"}, 400

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    job = Food.query.filter_by(id=food_id).first()

    if not job:
        return {"message": "food is not found"}, 400

    if mode == 'edit':
        one_value = len(list(set(data.values()))) == 1
        null = isinstance(None, type(list(set(data.values()))[0]))
        if one_value and null:
            return {"message": "kamu harus mempunyai data untuk mengedit"}, 400
        # if not ca.update_job:
        #     return {"message": "you not have permission"}, 403
        if not isinstance(None, type(data['name'])):
            job.name = data['name']
        if not isinstance(None, type(data['description'])):
            job.description = data['description']
        if not isinstance(None, type(data['start_time'])):
            job.start_time = data['start_time']
        if not isinstance(None, type(data['deadline'])):
            job.deadline = data['deadline']
        if not isinstance(None, type(data['category_id'])):
            food_ca_ = FoodCategory.query.filter_by(id=data['category_id']).first()
            if not food_ca_:
                return {"message": "category id is not found"}, 400
            job.category_id = data['category_id']
        if not isinstance(None, type(data['done'])):
            if not job.done:
                job.done = data['done']
            else:
                # if not ca.root_access:
                #     return {"error": "you can't edit done status for this job :)"}, 400
                job.done = data['done']

        try:
            job.commit()
        except:
            return {"message": "error to edit, tell you software engineer!!"}, 500
        return {"message": "success to edit"}
    if mode == 'delete':
        # if not ca.delete_job:
        #     return {"message": "you not have permission"}, 403
        try:
            job.delete()
        except:
            return {"message": "error to delete, tell you software engineer!!"}, 500
        return {"message": "success to delete"}
    return {'data': job.__serialize__(with_img=True)}


@jwt_required
def food_category(name, mode='create'):
    ca = FoodCategory.query.filter_by(name=name).first()
    store = Store.query.filter_by(owner=get_jwt_identity()).first()
    if not store:
        return {"error": "you have to create store first"}, 403
    if mode == 'delete':
        if not ca:
            return {"error": "kategori {} tidak ada".format(name)}, 400
        try:
            ca.delete()
        except:
            return {"error": "terjadi kesalahan saat menghapus, tanyakan masalah ini ke backend".format(name)}, 500
        return {"message": "sukses"}
    if ca:
        return {"error": "kategori sudah ada"}, 400
    food_ca_ = FoodCategory(name=name)
    try:
        food_ca_.commit()
    except:
        return {"message": "error untuk membuat, "
                           "perhatikan ketentuan pembuatan "
                           "kategori apakah sudah benar"}, 500
    return {"message": "success"}


@jwt_required
def food_category_list(page):
    if not page:
        page = 1
    try:
        page = int(page)
    except:
        return {"error": "parameter page must be integer"}, 400
    job_cat_list_ = FoodCategory.query.paginate(per_page=20, page=page)

    if not job_cat_list_.total:
        return {"message": "job category is empty"}, 204

    result = []
    for item in job_cat_list_.items:
        result.append({"id": item.id, "name": item.name})

    meta = {
        "total_data": job_cat_list_.total,
        "total_pages": job_cat_list_.pages,
        "total_data_per_page": job_cat_list_.per_page,
        "next": "?page={}".format(job_cat_list_.next_num) if job_cat_list_.has_next else None,
        "prev": "?page={}".format(job_cat_list_.prev_num) if job_cat_list_.has_prev else None
    }
    return {"data": result, "meta": meta}


@jwt_required
def users_of_food(food_id):
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user authentication is wrong"}, 400

    # ca = CategoryAccess.query.filter_by(id=user.category_access_id).first()
    # if not ca:
    #     return {"message": "you permission is not setup"}, 403

    job = Food.query.filter_by(id=food_id).first()

    if not job:
        return {"message": "job is not found"}, 400

    users = User\
        .query\
        .join(user_foods)\
        .join(Food)\
        .filter(Food.id == food_id)

    result = []

    if not users.first():
        result = None
    else:
        for user_ in users:
            result.append({'id': user_.id, "username": user_.username})

    job_detail = {"job": job.__serialize__(), "users": result}

    return {"data": job_detail}
