from flask import request, render_template

from app.middlewares.auth.login import user_login_check
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def home():
    cart_items_number = cart_items_counter()
    print(getattr(request, 'cart_id', None))
    return render_template('web/home/home.html', user_id=getattr(request, 'user_id', None),
                           cart_items_number=cart_items_number)
