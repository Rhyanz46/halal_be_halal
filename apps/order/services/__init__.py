from apps.order.models.cart import Cart, CartItem
from apps.user.models import User, UserDetail
from apps.food.models import Food
from flask_jwt_extended import jwt_required, get_jwt_identity


# @jwt_required
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

    for item in items:
        if "id" and "qty" not in item.keys():
            return {"message": "item must have id and qty"}, 400
        if not isinstance(int, type(item["id"])):
            return {"message": "id of item should be not null"}, 400
        if isinstance(int, type(item["qty"])):
            return {"message": "qty of item should be not null"}, 400
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

    cart = Cart()
    cart.cart_items = food_items
    user.user_detail.cart.append(cart)
    try:
        user.commit()
    except:
        return {"message": "can't save, tell you engineer"}, 500
    return {"data": "hello"}
