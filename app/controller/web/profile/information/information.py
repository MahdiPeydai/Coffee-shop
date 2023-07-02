from flask import render_template, request, flash, redirect, url_for

from app import db, model
from sqlalchemy import and_, func

from app.middlewares.auth.login import user_login_require

from app.forms import Profile


@user_login_require
def user_information(user_id):
    user = db.session.query(model.User.firstname, model.User.lastname, model.User.email, model.User.phone) \
        .filter_by(id=user_id).first()
    user_information = {
        'firstname': user[0],
        'lastname': user[1],
        'email': user[2],
        'phone': user[3]
    }
    return render_template('web/profile/information/information.html', user_information=user_information, user_id=user_id)


@user_login_require
def user_information_edit(user_id):
    user = db.session.query(model.User.firstname, model.User.lastname, model.User.email, model.User.phone) \
        .filter_by(id=user_id).first()
    placeholders = {
        'firstname': user[0],
        'lastname': user[1],
        'email': user[2],
        'phone': user[3]
    }
    form = Profile(data=placeholders)
    return render_template('web/profile/information/information_edit.html', form=form, user_id=user_id)


@user_login_require
def user_information_update(user_id):
    form = Profile()
    if form.validate:
        if request.form.get('_method') == 'PUT':
            user_check = db.session.query(model.User.id) \
                .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id) \
                .join(model.Role, model.user_role_association.c.role_id == model.Role.id) \
                .filter(and_(model.User.email == request.form['email'],
                             model.Role.name == 'shopper',
                             model.User.is_deleted == None,
                             model.User.id != user_id)).first()
            if user_check:
                flash('کاربر با این ایمیل قبلا ثبت شده', 'error')
                return redirect(url_for('user_information_edit'))

            user = db.session.query(model.User).get(user_id)
            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            user.email = request.form['email']
            user.phone = request.form['phone']
            db.session.commit()

            flash('تغییرات با موفقیت ذخیره شد ...', 'message')
            return redirect(url_for('user_information_edit'))


@user_login_require
def user_delete(user_id):
    user = db.session.query(model.User).get(user_id)
    user.is_deleted = func.current_timestamp()
    db.session.commit()

    return redirect(url_for('home'))
