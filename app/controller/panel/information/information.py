from app import app, db, model
from sqlalchemy import func, and_
from flask import request, redirect, render_template, url_for, flash
from app.forms import User, ChangePassword
from app.middlewares.auth.login import user_login_require
from app.middlewares.auth.permissions import permission_require
import hashlib


@user_login_require
@permission_require(['user.index'])
def admin_information():
    users = db.session.query(model.User.id, model.User.firstname, model.User.lastname, model.User.email,
                             model.User.phone, model.Role.name.label('role')) \
        .join(model.user_role_association, model.user_role_association.c.user_id == model.User.id) \
        .join(model.Role, model.Role.id == model.user_role_association.c.role_id) \
        .filter(model.User.is_deleted == None) \
        .order_by(model.User.id)
    data = {}
    for id, firstname, lastname, email, phone, role in users:
        if id not in data.keys():
            data[id] = {
                'name': f'{firstname} {lastname}',
                'email': email,
                'phone': phone,
                'role': role
            }
    return render_template('panel/information/admin_information.html', data=data)


@user_login_require
@permission_require(['user.store'])
def admin_user_store():
    form = User()
    roles = db.session.query(model.Role.id, model.Role.name)

    role = [('', 'Choose User Role ...')]
    for id, name in roles:
        role.append((id, name))
    form.role.choices = role
    return render_template('panel/information/user_store.html', form=form)


@user_login_require
@permission_require(['user.store'])
def admin_user_create():
    form = User()
    roles = db.session.query(model.Role.id, model.Role.name)

    role = [('', 'Choose User Role ...')]
    for id, name in roles:
        role.append((id, name))
    form.role.choices = role
    if form.validate:
        user_id = db.session.query(model.User.id) \
            .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id) \
            .join(model.Role, model.user_role_association.c.role_id == model.Role.id) \
            .filter(and_(model.User.email == request.form['email'],
                         model.Role.id == request.form['role'],
                         model.User.is_deleted == None)).first()

        if user_id:
            flash('کاربر با این ایمیل قبلا ثبت شده', 'error')
            return redirect(url_for('admin_user_store'))

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
        new_user_id = new_user.id

        new_role_query = model.user_role_association.insert().values(user_id=new_user_id, role_id=request.form['role'])
        db.session.execute(new_role_query)
        db.session.commit()
        flash('کاربر با موفقیت ایجاد شد', 'message')
        return redirect(url_for('admin_user'))


@user_login_require
@permission_require(['user.edit'])
def admin_user_edit(id):
    user = db.session.query(model.User.firstname, model.User.lastname, model.User.email,
                            model.User.phone, model.Role.id.label('role')) \
        .join(model.user_role_association, model.user_role_association.c.user_id == model.User.id) \
        .join(model.Role, model.Role.id == model.user_role_association.c.role_id) \
        .filter(model.User.id == id).first()
    placeholders = {
        'firstname': user[0],
        'lastname': user[1],
        'email': user[2],
        'phone': user[3],
        'role': user[4]
    }
    form = User(data=placeholders)

    roles = db.session.query(model.Role.id, model.Role.name)
    choices = [('', 'Choose User Role ...')]
    for role in roles:
        choices.append((role[0], role[1]))
    form.role.choices = choices
    return render_template('panel/information/user_edit.html', form=form, user_id=id)


@user_login_require
@permission_require(['user.edit'])
def admin_user_update(id):
    form = User()
    form.password.validators = []
    form.confirm_password.validators = []
    roles = db.session.query(model.Role.id, model.Role.name)
    choices = [('', 'Choose User Role ...')]
    for role in roles:
        choices.append((role[0], role[1]))
    form.role.choices = choices
    if form.validate:
        if request.form.get('_method') == 'PUT':
            user_check = db.session.query(model.User.id) \
                .join(model.user_role_association, model.User.id == model.user_role_association.c.user_id) \
                .join(model.Role, model.user_role_association.c.role_id == model.Role.id) \
                .filter(and_(model.User.email == request.form['email'],
                             model.Role.id == request.form['role'],
                             model.User.is_deleted == None,
                             model.User.id != id)).first()

            if user_check:
                flash('کاربر با این ایمیل قبلا ثبت شده', 'error')
                return redirect(url_for('admin_user_edit', id=id))

            user = db.session.query(model.User).get(id)
            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            user.phone = request.form['phone']
            user.email = request.form['email']
            db.session.commit()

            update_role_query = model.user_role_association.update().filter_by(user_id=id) \
                .values(role_id=request.form['role'])
            db.session.execute(update_role_query)
            db.session.commit()

            flash('تغییرات با موفقیت انجام شد', 'message')
            return redirect(url_for('admin_user_edit', id=id))


@user_login_require
@permission_require(['user.edit'])
def admin_user_password_edit(id):
    form = ChangePassword()
    return render_template('panel/information/user_password_edit.html', form=form, user_id=id)


@user_login_require
@permission_require(['user.edit'])
def admin_user_password_update(user_id, id):
    form = ChangePassword()
    if form.validate:
        if request.form.get('_method') == 'PUT':
            old_password = request.form['old_password']
            old_password = old_password.encode()
            old_hashed_password = (hashlib.sha256(old_password)).hexdigest()

            password_check = db.session.query(model.User).filter(and_(model.User.id == id,
                                                                      model.User.password == old_hashed_password)).first()

            if not password_check:
                flash('رمز عبور صحیح نیست', 'error')
                return redirect(url_for('admin_user_password_edit', id=id))
            password = request.form['password']
            password = password.encode()
            hashed_password = (hashlib.sha256(password)).hexdigest()

            user = db.session.query(model.User).get(id)
            user.password = hashed_password
            db.session.commit()
            flash('رمز عبور با موفقیت تغییر کرد', 'message')
            return redirect(url_for('admin_user_edit', id=id))


@user_login_require
@permission_require(['user.destroy'])
def admin_user_delete(id):
    user = db.session.query(model.User).get(id)
    user.is_deleted = func.current_timestamp()
    db.session.commit()
    return redirect(url_for('admin_user'))
