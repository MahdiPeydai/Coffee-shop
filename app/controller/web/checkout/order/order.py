from flask import redirect, url_for, request, make_response

from app import db, model

from app.middlewares.auth.login import user_login_require
from app.middlewares.cart.cart import cart_check


@user_login_require
@cart_check
def order_create():
    cart_id = getattr(request, 'cart_id', None)
    user_id = getattr(request, 'user_id', None)
    address = model.Address.query.filter_by(user_id=user_id).first()

    order = model.Order(
        user_id=user_id,
        address_id=address.id,
    )
    db.session.add(order)
    db.session.commit()
    order_id = order.id

    cart_items = model.CartItem.query.filter_by(cart_id=cart_id).all()

    for item in cart_items:
        product = item.product

        order_item = model.OrderItem(
            order_id=order_id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
            discount=product.discount
        )
        db.session.add(order_item)
        db.session.commit()

    order_items = model.OrderItem.query.filter_by(order_id=order_id).all()

    total_price = 0
    for item in order_items:
        product = item.product
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price

        total_price += final_price * item.quantity

    payment = model.Payment(
        order_id=order_id,
        total_amount=total_price
    )

    db.session.add(payment)
    db.session.commit()

    db.session.query(model.CartItem).filter_by(cart_id=cart_id).delete()
    db.session.query(model.Cart).filter_by(id=cart_id).delete()
    db.session.commit()

    resp = make_response(redirect(url_for('payment_data_post', payment_id=payment.id)))
    resp.set_cookie('cart', '', expires=0)

    return resp
