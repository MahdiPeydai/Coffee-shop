from flask import request, render_template

from app import db, model

from app.middlewares.auth.login import user_login_check
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def home():
    cart_items_number = cart_items_counter()
    offer = model.Product.query.filter_by(is_deleted=None).order_by(model.Product.discount.desc()).limit(4).all()
    offer_products = []
    for product in offer:
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price
        offer_products.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'discount': product.discount,
            'final_price': final_price
        })

    most_sail = model.Product.query.join(model.OrderItem).group_by(model.Product.id).order_by(
        db.func.sum(model.OrderItem.quantity).desc()).limit(4).all()
    most_sailed_products = []
    for product in most_sail:
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price
        most_sailed_products.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'discount': product.discount,
            'final_price': final_price
        })

    return render_template('web/home/home.html', user_id=getattr(request, 'user_id', None),
                           most_sailed_products=most_sailed_products, cart_items_number=cart_items_number,
                           offer_products=offer_products)
