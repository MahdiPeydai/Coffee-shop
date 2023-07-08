from flask import redirect, url_for, request, make_response

from app import db, model

from app.middlewares.auth.login import user_login_require


@user_login_require
def order_create(cart_id):
    user_id = getattr(request, 'user_id', None)
    address = model.Address.query.filter_by(user_id=user_id).first()

    total_price = 0
    cart_items = model.CartItem.query.filter_by(cart_id=cart_id).all()
    for item in cart_items:
        product = item.product
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price

        total_price += final_price * item.quantity

    order = model.Order(
        user_id=user_id,
        payment='pending',
        address_id=address.id,
        total=total_price
    )
    db.session.add(order)
    db.session.commit()

    order_id = order.id

    for item in cart_items:
        product = item.product

        if product.discount:
            discount = product.discount
        else:
            discount = None

        order_item = model.OrderItem(
            order_id=order_id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
            discount=discount
        )
        db.session.add(order_item)
        db.session.commit()
    return redirect(url_for('payment_data_send', order_id=order_id))
