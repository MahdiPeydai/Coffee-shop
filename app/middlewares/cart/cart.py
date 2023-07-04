from flask import request, redirect, url_for, make_response
from app import app

from functools import wraps

from app import db, model

import jwt


def cart_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'cart' in request.cookies:
            token = request.cookies.get('cart')
            cart_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            cart_id = cart_id['cart_id']

            cart = db.session.query(model.Cart).get(cart_id)
            if (not cart.user_id) and (getattr(request, 'user_id', None)):
                cart.user_id = getattr(request, 'user_id', None)
                db.session.commit()
            request.cart_id = cart_id

            return func(*args, **kwargs)
        else:
            user_id = getattr(request, 'user_id', None)
            cart = model.Cart(
                user_id=user_id
            )
            db.session.add(cart)
            db.session.commit()

            cart_id = cart.id
            request.cart_id = cart_id
            resp = make_response(func(*args, **kwargs))
            token = jwt.encode({'cart_id': cart_id}, app.config['SECRET_KEY'], algorithm='HS256')
            resp.set_cookie('cart', token)
            return resp
    return decorator
