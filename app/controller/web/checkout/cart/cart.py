from flask import render_template, redirect, request, flash

from app import db, model
from sqlalchemy import and_

from app.middlewares.auth.login import user_login_check
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def cart():
    cart_items_number = cart_items_counter()
    cart_id = getattr(request, 'cart_id', None)
    if cart_items_number == 0:
        cart_status = 'empty'
        return render_template('web/checkout/cart/cart.html', user_id=getattr(request, 'user_id', None),
                               cart_items_number=cart_items_number, cart_status=cart_status)
    else:
        cart_status = 'full'
        cart_items_tuple = db.session.query(model.Product.id, model.Product.name, model.CartItem.quantity,
                                            model.Product.price, model.Product.discount) \
            .join(model.Product, model.Product.id == model.CartItem.product_id) \
            .filter(model.CartItem.cart_id == cart_id).all()
        cart_items = []
        for id, name, quantity, price, discount in cart_items_tuple:
            if discount:
                final_price = int(price * ((100 - discount) / 100))
            else:
                final_price = price

            cart_items.append(
                {
                    'id': id,
                    'name': name,
                    'quantity': quantity,
                    'price': price,
                    'discount': discount,
                    'final_price': final_price
                }
            )

        cart_price = {
            'cart_total_price': 0,
            'cart_total_discount': 0,
            'cart_total_final_price': 0
        }
        for item in cart_items:
            cart_price['cart_total_price'] += item['price']
            cart_price['cart_total_discount'] += (item['price'] - item['final_price'])
            cart_price['cart_total_final_price'] += item['final_price']

        return render_template('web/checkout/cart/cart.html', user_id=getattr(request, 'user_id', None),
                               cart_items_number=cart_items_number, cart_status=cart_status,
                               cart_items=cart_items, cart_price=cart_price)


@user_login_check
@cart_check
def cart_item_store(product_id):
    cart_id = getattr(request, 'cart_id', None)
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
def cart_item_destroy(product_id):
    cart_id = getattr(request, 'cart_id', None)
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
