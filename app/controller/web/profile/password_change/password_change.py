from flask import render_template, request, flash, redirect, url_for

from app import db, model
from sqlalchemy import and_

from app.middlewares.auth.login import user_login_require

from app.forms import ChangePassword

import hashlib


@user_login_require
def user_password_edit(user_id):
    form = ChangePassword()
    return render_template('web/profile/password_change/password_change.html', form=form, user_id=user_id)


@user_login_require
def user_password_update(user_id):
    form = ChangePassword()
    if form.validate:
        if request.form.get('_method') == 'PUT':
            # password_check_sql = 'SELECT password ' \
            #                      'FROM user ' \
            #                      'WHERE id = %s'
            # password_check_val = (user_id,)
            # curs.execute(password_check_sql, password_check_val)

            old_password = request.form['old_password']
            old_password = old_password.encode()
            old_hashed_password = (hashlib.sha256(old_password)).hexdigest()

            password_check = db.session.query(model.User).filter(and_(model.User.id == user_id,
                                                                      model.User.password == old_hashed_password)).first()

            if not password_check:
                flash('رمز عبور صحیح نیست', 'error')
                return redirect(url_for('user_password_edit'))

            # password_update_sql = 'UPDATE user ' \
            #                       'SET password=%s ' \
            #                       'WHERE id=%s'
            # password_update_val = (user_hashed_password, user_id)
            # curs.execute(password_update_sql, password_update_val)

            password = request.form['password']
            password = password.encode()
            hashed_password = (hashlib.sha256(password)).hexdigest()

            user = db.session.query(model.User).get(user_id)
            user.password = hashed_password
            db.session.commit()
            flash('رمز عبور با موفقیت تغییر کرد', 'message')
            return redirect(url_for('user_password_edit'))
    if 'confirm_password' in form.errors.keys():
        flash('رمز عبور جدید معتبر نمیباشد ...', 'error')
        return redirect(url_for('user_password_edit'))
