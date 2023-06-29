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

        # with open('app/data/users_information.json', 'r+') as information_file:
        #     users = json.load(information_file)

        # find_user_sql = 'SELECT id ' \
        #                 'FROM users ' \
        #                 'WHERE email = %s AND password = %s'
        # find_user_val = (user_email, user_password)
        # curs.execute(find_user_sql, find_user_val)
        # user_id = curs.fetchone()['id']

        user_id = db.session.query(model.User.id) \
            .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id) \
            .join(model.Role, model.user_role_association.c.role_id == model.Role.id) \
            .filter(and_(model.User.email == request.form['email'],
                         model.User.is_deleted == None,
                         model.User.password == user_password,
                         model.Role.name == 'shopper')).first()

        if user_id:
            resp = make_response(redirect(url_for('home')))
            token = jwt.encode({'user_id': user_id[0]}, app.config['SECRET_KEY'], algorithm='HS256')
            resp.set_cookie('user_token', token)
            return resp
        else:
            flash('ایمیل یا رمز عبور وارد شده صحیح نمی‌باشند', 'error')
            return redirect(url_for('user_login'))
    return render_template('auth/user_login.html', form=form)
