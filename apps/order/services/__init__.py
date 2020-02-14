from flask import request

from apps.order.models.cart import Cart, CartItem
from apps.user.models import User, UserDetail
from apps.food.models import Food
from apps.order.models import Order, OrderLocationTracked
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required
def post_order(data):
    user_id = data["user_id"]
    notes = data['notes']
    order_time = data['order_time']
    items = data['items']
    deliver_to = data['deliver_to']
    order_loc = data['order_loc']

    food_items = []

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return {"message": "user id is not found"}, 400

    if not items:
        return {"message": "items must be not null"}, 400

    if list(order_loc.keys()) != ['latitude', 'longitude', 'accuracy']:
        return {"message": "order_loc object is not valid key"}, 400

    if type(order_loc['latitude']) != float and type(order_loc['latitude']) != int:
        return {"message": "latitude of order_loc object is not valid type"}, 400

    if type(order_loc['longitude']) != float and type(order_loc['longitude']) != int:
        return {"message": "longitude of order_loc object is not valid type"}, 400

    if type(order_loc['accuracy']) != float and type(order_loc['accuracy']) != int:
        return {"message": "accuracy of order_loc object is not valid type"}, 400

    if list(deliver_to.keys()) != ['latitude', 'longitude', 'accuracy', 'is_pinned']:
        return {"message": "deliver_to object is not valid key"}, 400

    if type(deliver_to['latitude']) != float and type(deliver_to['latitude']) != int:
        return {"message": "latitude of deliver_to object is not valid type"}, 400

    if type(deliver_to['longitude']) != float and type(deliver_to['longitude']) != int:
        return {"message": "longitude of deliver_to object is not valid type"}, 400

    if type(deliver_to['accuracy']) != float and type(deliver_to['accuracy']) != int:
        return {"message": "accuracy of deliver_to object is not valid type"}, 400

    if type(deliver_to['is_pinned']) != bool:
        return {"message": "is_pinned of deliver_to object is not valid type"}, 400

    for item in items:
        if "id" and "qty" not in item.keys():
            return {"message": "item must have id and qty"}, 400
        if int != type(item["id"]):
            return {"message": "id of item should be integer"}, 400
        if int != type(item["qty"]):
            return {"message": "qty of item should be integer"}, 400
        food = Food.query.get(item["id"])
        if not food:
            return {"message": "food id={} is not found".format(item["id"])}, 400
        if food.stock < item["qty"]:
            return {"message": "stock not enough for {}, avalaible {} ".format(food.name, food.stock)}, 400
        item = CartItem(
            qty=item["qty"],
            food_id=item["id"]
        )
        food_items.append(item)

    order_loc = OrderLocationTracked(
        latitude=order_loc['latitude'],
        longitude=order_loc['longitude'],
        accuracy=order_loc['accuracy']
    )

    deliver_to = OrderLocationTracked(
        latitude=deliver_to['latitude'],
        longitude=deliver_to['longitude'],
        accuracy=deliver_to['accuracy'],
        is_pinned=deliver_to['is_pinned']
    )

    order = Order(
        order_time=order_time,
        order_loc=order_loc,
        deliver_to=deliver_to,
        notes=notes,
        cart=Cart()
    )
    order.cart.cart_items = food_items
    user.user_detail.orders.append(order)
    try:
        user.commit()
    except:
        return {"message": "can't save, tell you engineer"}, 500
    return {"message": "success", "data": order.get(detail=True)}


@jwt_required
def my_order_list(page, per_page):
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        return {"message": "user id is not found"}, 400
    order = Order.query.join(UserDetail).filter(
        UserDetail.id == user.user_detail.id
    ).paginate(page=page, per_page=per_page)
    orders = []
    for item in order.items:
        orders.append(item.get())
    meta = {
        "total_data": order.total,
        "total_pages": order.pages,
        "total_data_per_page": order.per_page,
        "next": "{}?page={}".format(request.url_rule, order.next_num) if order.has_next else None,
        "prev": "{}?page={}".format(request.url_rule, order.prev_num) if order.has_prev else None
    }
    return {"meta": meta, "data": orders}
