from app import db, model
from sqlalchemy import and_
from flask import request, redirect, render_template, url_for, flash
from app.forms import Permission
from app.controller.middlewares.auth.login import admin_login_require
from app.controller.middlewares.auth.permissions import permission_require


@admin_login_require
@permission_require(['permission'])
def admin_permission():
    data = db.session.query(model.Permission.id, model.Permission.name, model.Permission.description)
    return render_template('panel/permission/admin_permission.html', data=data)


@admin_login_require
@permission_require(['permission', 'permission_crud'])
def permission_create():
    form = Permission()
    return render_template('panel/permission/permission_create.html', form=form)


@admin_login_require
@permission_require(['permission', 'permission_crud'])
def permission_store():
    form = Permission()
    if form.validate:
        permission_check = db.session.query(model.Permission.name)\
            .filter_by(name=request.form['permission_name']).first()

        if permission_check:
            flash('Permission با این نام وجود دارد', 'error')
            return redirect(url_for('permission_create'))

        permission = model.Permission(
            name=request.form['permission_name'],
            description=request.form['permission_description']
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permission با موفقیت ایجاد شد', 'message')
        return redirect(url_for('admin_permission'))


@admin_login_require
@permission_require(['permission', 'permission_crud'])
def permission_edit(permission_id):
    permission = db.session.query(model.Permission.name, model.Permission.description) \
        .filter_by(id=permission_id).first()
    placeholders = {
        'permission_name': permission[0],
        'permission_description': permission[1]
    }
    form = Permission(data=placeholders)
    return render_template('panel/permission/permission_edit.html', form=form, permission_id=permission_id)


@admin_login_require
@permission_require(['permission', 'permission_crud'])
def permission_update(permission_id):
    form = Permission()
    if form.validate:
        if request.form.get('_method') == 'PUT':
            permission_check = db.session.query(model.Permission.name).filter(and_(
                model.Permission.name == request.form['permission_name'],
                model.Permission.id != permission_id
            )).first()

            if permission_check:
                flash('Permission با این نام وجود دارد', 'error')
                return redirect(url_for('admin_permission'))

            permission = db.session.query(model.Permission).get(permission_id)
            permission.name = request.form['permission_name']
            permission.description = request.form['permission_description']
            db.session.commit()
            flash('تغییرات با موفقیت انجام شد', 'message')
            return redirect(url_for('permission_edit', permission_id=permission_id))


@admin_login_require
@permission_require(['permission', 'permission_crud'])
def permission_delete(permission_id):
    db.session.query(model.Permission).filter_by(id=permission_id).delete()
    db.session.commit()
    flash('permission با موفقیت حذف شد', 'message')
    return redirect(url_for('admin_permission'))
