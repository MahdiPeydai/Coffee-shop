from flask import render_template

from app.middlewares.auth.login import user_login_check
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def home(user_id, cart_id):
    cart_items_number = cart_items_counter(cart_id)
    return render_template('web/home/home.html', user_id=user_id, cart_items_number=cart_items_number)
