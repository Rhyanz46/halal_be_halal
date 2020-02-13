from apps.order.models.cart import Cart, CartItem
from apps.user.models import User
from apps.food.models import Food
from apps.order.models import Order, OrderLocationTracked
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

    if list(order_loc.keys()) != ['latitude', 'longitude', 'accuracy']:
        return {"message": "order_loc object is not valid key"}, 400

    # pengecekan tipe data di setiap value dari key order_loc

    if list(deliver_to.keys()) != ['latitude', 'longitude', 'accuracy', 'is_pinned']:
        return {"message": "deliver_to object is not valid key"}, 400

    # pengecekan tipe data di setiap value dari key deliver_to

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

    )

    deliver_to = OrderLocationTracked(

    )

    cart = Cart()
    order = Order(
        user_id=user_id,
        order_time=order_time,
        order_loc=order_loc,
        deliver_to=deliver_to,
        notes=notes
    )
    order.cart = cart
    order.cart.cart_items = food_items
    user.user_detail.orders.append(order)
    try:
        user.commit()
    except:
        return {"message": "can't save, tell you engineer"}, 500
    return {"data": "hello"}
