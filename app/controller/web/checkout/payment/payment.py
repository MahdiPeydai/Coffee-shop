from flask import redirect, url_for, request, render_template, make_response

import requests

from app import db, model

from app.middlewares.auth.login import user_login_require
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_require
def payment_data_send(order_id):
    order = model.Order.query.filter_by(id=order_id).first()

    url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "merchant_id": "349F54A1-2DCF-4E2F-9A2D-98558951968A",
        "amount": order.total * 10,
        "description": "بهنام کافه",
        "callback_url": url_for('payment_result', order_id=order_id, _external=True),
        "metadata": {
            'mobile': order.user.phone,
            'email': order.user.email,
            'order_id': order_id
        }
    }
    while True:
        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            response_json = response.json()
            data = response_json['data']
            authority = data['authority']
            break

    return redirect(f'https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}')


@user_login_require
@cart_check
def payment_result(order_id):
    payment_status = request.args.get('Status')
    offer = model.Product.query.filter_by(is_deleted=None).order_by(model.Product.discount.desc()).limit(4).all()
    offer_products = []
    for product in offer:
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price

        image = model.ProductImage.query.filter_by(product_id=product.id).first()

        offer_products.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'discount': product.discount,
            'final_price': final_price,
            'image': image.name
        })
    if payment_status == 'OK':
        order = model.Order.query.filter_by(id=order_id).first()
        url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "merchant_id": "349F54A1-2DCF-4E2F-9A2D-98558951968A",
            "amount": order.total * 10,
            "authority": request.args.get('Authority')
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_json = response.json()
            data = response_json['data']
            if data['code'] == 100:
                ref_id = data['ref_id']

                order = model.Order.query.get(order_id)
                order.payment = 'successful'
                db.session.commit()

                cart_id = getattr(request, 'cart_id', None)
                db.session.query(model.CartItem).filter_by(cart_id=cart_id).delete()
                db.session.query(model.Cart).filter_by(id=cart_id).delete()
                db.session.commit()

                resp = make_response(render_template('web/checkout/payment/payment.html', payment_status=payment_status,
                                                     order_id=order_id, offer_products=offer_products, ref_id=ref_id,
                                                     user_id=getattr(request, 'user_id', None)))
                resp.set_cookie('cart', '', expires=0)
    else:
        order = model.Order.query.get(order_id)
        order.payment = 'failed'
        db.session.commit()

        cart_items_number = cart_items_counter()

        return render_template('web/checkout/payment/payment.html', user_id=getattr(request, 'user_id', None),
                               payment_status=payment_status, order_id=order_id, offer_products=offer_products,
                               cart_items_number=cart_items_number)
