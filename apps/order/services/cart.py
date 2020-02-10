from apps.order.models.cart import Cart, CartItem
from apps.user.models import User, UserDetail
from apps.food.models import Food
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required
def post_cart(data):
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not data['amount']:
        data['amount'] = 1
    if not user:
        return {"message": "user authentication is wrong"}, 400
    if not user.user_detail.cart:
        user.user_detail.cart = Cart()
        user.commit()
    food = Food.query.get(data['food_id'])
    if not food:
        return {"message": "food is not found"}, 400
    cart_item = CartItem(
        amount=data['amount']
    )
    cart_item.foods.append(food)
    cart_item.commit()
    user.user_detail.cart.cart_items.append(cart_item)
    user.commit()
    return {"data": "hello"}
