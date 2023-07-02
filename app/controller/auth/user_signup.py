from flask import render_template, make_response, redirect, url_for, request, flash

from app import app, db, model
from sqlalchemy import and_

from app.forms import UserRegister

import jwt
import hashlib


def user_register():
    form = UserRegister(request.form)
    if request.method == 'POST' and form.validate:
        # account_check_sql = 'SELECT * FROM users WHERE email = %s'
        # account_check_val = (request.form['email'],)
        # curs.execute(account_check_sql, account_check_val)
        # account_check = curs.fetchall()

        user_check = db.session.query(model.User)\
            .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id)\
            .join(model.Role, model.user_role_association.c.role_id == model.Role.id)\
            .filter(and_(model.User.email == request.form['email'],
                         model.User.is_deleted != None)).first()

        if user_check:
            flash('کاربر با ایمیل وارد شده وجود ندارد', 'error')
            return redirect(url_for('user_register'))

        user_password = request.form['password']
        user_password = user_password.encode()
        user_hashed_password = (hashlib.sha256(user_password)).hexdigest()

        new_user = model.User(
            firstname=request.form['firstname'],
            lastname=request.form['lastname'],
            email=request.form['email'],
            phone=request.form['phone'],
            password=user_hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id

        role_id = db.session.query(model.Role.id).filter_by(name='shopper').first()
        user_role = model.user_role_association.insert().values(user_id=user_id, role_id=role_id[0])
        db.session.execute(user_role)
        db.session.commit()

        resp = make_response(redirect(url_for('home')))
        token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], 'HS256')
        resp.set_cookie('user_token', token)
        return resp
    return render_template('auth/user_register.html', form=form)
