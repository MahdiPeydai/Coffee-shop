from flask import redirect, url_for, request, render_template, make_response

import requests

from app import db, model

from app.middlewares.auth.login import user_login_require
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_require
def payment_data_post(payment_id):
    payment = model.Payment.query.filter_by(id=payment_id).first()

    transaction = model.Transaction(
        payment_id=payment_id,
    )
    db.session.add(transaction)
    db.session.commit()

    url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "merchant_id": "349F54A1-2DCF-4E2F-9A2D-98558951968A",
        "amount": payment.total_amount,
        "description": "بهنام کافه",
        "callback_url": url_for('transaction_result', transaction_id=transaction.id, _external=True),
        "metadata": {
            'mobile': payment.order.user.phone,
            'email': payment.order.user.email
        }
    }
    while True:
        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            response_json = response.json()
            data = response_json['data']
            authority = data['authority']
            break

    transaction.authority = authority
    db.session.commit()


    return redirect(f'https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}')


@user_login_require
@cart_check
def transaction_result(transaction_id):
    transaction_status = request.args.get('Status')

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

    transaction = model.Transaction.query.filter_by(id=transaction_id).first()
    if transaction_status == 'OK':
        url = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "merchant_id": "349F54A1-2DCF-4E2F-9A2D-98558951968A",
            "amount": transaction.payment.total_amount,
            "authority": transaction.authority
        }
        while True:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response_json = response.json()
                data = response_json['data']
                if data['code'] == 100 or data['code'] == 101:
                    transaction.status = 'successful'
                    transaction.details = 'پرداخت با موفقیت انجام شد'
                    db.session.commit()
                else:
                    transaction.status = 'fail'
                    transaction.details = 'مشکلی در عملیات پرداخت بوجود آمده، مبلغ کسر شده بعد از ۴۸ساعت به حساب شما باز میگردد'
                    db.session.commit()
                break
    else:
        transaction.status = 'fail'
        transaction.details = 'عملیات پرداخت لغو شد'
        db.session.commit()
    return render_template('web/checkout/payment/payment.html', transaction=transaction,
                           offer_products=offer_products, user_id=getattr(request, 'user_id', None))