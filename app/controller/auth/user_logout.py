from flask import make_response, redirect, url_for

from app import app, db, model

import jwt


def user_logout():
    cart = model.Cart(
        user_id=None
    )
    db.session.add(cart)
    db.session.commit()
    cart_id = cart.id
    token = jwt.encode({'cart_id': cart_id}, app.config['SECRET_KEY'], algorithm='HS256')

    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('cart', token)
    resp.set_cookie('user', '', expires=0)
    return resp
