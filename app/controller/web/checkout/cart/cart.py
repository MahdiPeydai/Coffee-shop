from flask import render_template, redirect, request, flash

from app import db, model
from sqlalchemy import and_

from app.middlewares.auth.login import user_login_check
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def cart(user_id, cart_id):
    cart_items_number = cart_items_counter(cart_id)
    if cart_items_number == 0:
        cart_status = 'empty'
        return render_template('web/checkout/cart/cart.html', user_id=user_id, cart_items_number=cart_items_number,
                               cart_status=cart_status)
    else:
        cart_status = 'full'
        cart_items_tuple = db.session.query(model.CartItem.quantity, model.Product.id, model.Product.name,
                                            model.Product.price, model.Product.discount) \
            .join(model.Product, model.Product.id == model.CartItem.product_id) \
            .filter(model.CartItem.cart_id == cart_id).all()
        cart_items = []
        for item in cart_items_tuple:
            cart_items.append(
                {
                    'quantity': item[0],
                    'id': item[1],
                    'name': item[2],
                    'price': item[3],
                    'discount': item[4]
                }
            )
        cart_price = {
            'cart_total_price': 0,
            'cart_total_discount': 0,
            'cart_total_discounted_price': 0
        }
        for item in cart_items:
            cart_price['cart_total_price'] += item['price']
            cart_price['cart_total_discount'] += int((item['discount'] * item['price'])/100)
            cart_price['cart_total_discounted_price'] += int(((100 - item['discount']) * item['price'])/100)

        return render_template('web/checkout/cart/cart.html', user_id=user_id, cart_items_number=cart_items_number,
                               cart_status=cart_status, cart_items=cart_items, cart_price=cart_price)


@user_login_check
@cart_check
def cart_item_store(user_id, cart_id, product_id):
    cart_item_check = db.session.query(model.CartItem.id, model.CartItem.quantity)\
        .filter(and_(model.CartItem.cart_id == cart_id, model.CartItem.product_id == product_id)).first()
    if cart_item_check:
        product_quantity = db.session.query(model.Product.quantity).filter_by(id=product_id).first()
        if product_quantity[0] == cart_item_check[1]:
            flash('موجودی کافی نیست...', 'error')
            return redirect(request.referrer)
        item = db.session.query(model.CartItem).get(cart_item_check[0])
        item.quantity += 1
        db.session.commit()
    else:
        new_item = model.CartItem(
            cart_id=cart_id,
            product_id=product_id
        )
        db.session.add(new_item)
        db.session.commit()
    return redirect(request.referrer)


@user_login_check
@cart_check
def cart_item_delete(user_id, cart_id, product_id):
    item_quantity_check = db.session.query(model.CartItem.id, model.CartItem.quantity).filter(
        and_(model.CartItem.cart_id == cart_id,
             model.CartItem.product_id == product_id)).first()
    if item_quantity_check[1] == 1:
        db.session.query(model.CartItem).filter(and_(model.CartItem.cart_id == cart_id,
                                                     model.CartItem.product_id == product_id)).delete()
        db.session.commit()
    else:
        item = db.session.query(model.CartItem).get(item_quantity_check[0])
        item.quantity -= 1
        db.session.commit()
    return redirect(request.referrer)
