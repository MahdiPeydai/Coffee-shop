from flask import render_template, make_response, redirect, url_for, request, flash

from app import app, db, model

from app.forms import UserLogin

from sqlalchemy import and_

import jwt
import hashlib


def user_login():
    form = UserLogin()
    if request.method == 'POST':
        user_password = request.form['password']
        user_password = user_password.encode()
        user_password = (hashlib.sha256(user_password)).hexdigest()

        user = db.session.query(model.User) \
            .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id) \
            .join(model.Role, model.user_role_association.c.role_id == model.Role.id) \
            .filter(and_(model.User.email == request.form['email'],
                         model.User.is_deleted == None,
                         model.User.password == user_password)).first()
        user_id = user.id

        if user_id:
            user_token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], algorithm='HS256')
            cart = db.session.query(model.Cart).filter_by(user_id=user_id).first()

            token = request.cookies.get('cart')
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('user', user_token)
            if token and cart:
                cart_token = jwt.encode({'cart_id': cart.id}, app.config['SECRET_KEY'], algorithm='HS256')
                old_cart = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                old_cart_id = old_cart['cart_id']
                model.CartItem.query.filter_by(cart_id=old_cart_id)\
                    .update({model.CartItem.cart_id: cart.id})
                db.session.commit()
                model.Cart.query.filter_by(id=old_cart_id).delete()
                db.session.commit()
                resp.set_cookie('cart', cart_token)

            return resp
        else:
            flash('ایمیل یا رمز عبور وارد شده صحیح نمی‌باشند', 'error')
            return redirect(url_for('user_login'))
    return render_template('auth/user_login.html', form=form)
