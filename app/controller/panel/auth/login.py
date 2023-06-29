from app import app, db, model
from sqlalchemy import and_, or_
from flask import request, make_response, redirect, render_template, url_for, flash
from app.forms import AdminLogin
import hashlib
import jwt


def admin_login():
    form = AdminLogin()
    if request.method == 'POST':
        user_password = request.form['password']
        user_password = user_password.encode()
        user_password = (hashlib.sha256(user_password)).hexdigest()

        user_id = db.session.query(model.User.id) \
            .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id) \
            .join(model.Role, model.user_role_association.c.role_id == model.Role.id) \
            .filter(and_(model.User.email == request.form['email'],
                         model.User.password == user_password,
                         model.Role.name != 'shopper')).first()

        if user_id:
            user_id = user_id[0]
            resp = make_response(redirect(url_for('panel')))
            token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], 'HS256')
            resp.set_cookie('admin_token', token)
            return resp
        else:
            flash('ایمیل یا رمز عبور نا معتبر است', 'error')
            return redirect(url_for('admin_login'))
    return render_template('panel/auth/panel_login.html', form=form)


def admin_logout():
    resp = make_response(redirect(url_for('admin_login')))
    resp.set_cookie('admin_token', '', expires=0)
    return resp
