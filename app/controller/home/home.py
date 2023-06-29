from flask import render_template, request

from app import db, model

from app.controller.middlewares.auth.login import user_login_check
from app.controller.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def home(user_id, cart_id):
    cart_items_number = cart_items_counter(cart_id)
    return render_template('home/home.html', user_id=user_id, cart_items_number=cart_items_number)
