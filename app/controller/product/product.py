from flask import render_template

from app import db, model
from sqlalchemy import and_

from app.controller.middlewares.cart.cart import cart_check
from app.controller.middlewares.auth.login import user_login_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def product(user_id, cart_id, product_id):
    cart_items_number = cart_items_counter(cart_id)

    product_tuple = db.session.query(model.Product.id, model.Product.name, model.Product.quantity, model.Product.price,
                                     model.Product.discount).filter_by(id=product_id).first()
    product_information = {
        'id': product_tuple[0],
        'name': product_tuple[1],
        'quantity': product_tuple[2],
        'price': product_tuple[3],
        'discount': product_tuple[4],
    }
    if product_information['discount']:
        product_information['discounted_price'] = int(product_information['price'] * ((100 - product_information['discount'])/100))
    else:
        product_information['discounted_price'] = product_information['price']

    cart = db.session.query(model.CartItem.quantity).filter(and_(model.CartItem.cart_id == cart_id,
                                                                 model.CartItem.product_id == product_tuple[0])).first()
    if cart:
        item_quantity = cart[0]
    else:
        item_quantity = None
    if product_tuple[2] < 10:
        limit = True
    else:
        limit = False
    return render_template('product/product.html', user_id=user_id, cart_items_number=cart_items_number,
                           product=product_information,item_quantity=item_quantity, limit=limit)
