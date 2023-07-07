from app import app, db, model
from sqlalchemy import and_
from flask import request, redirect, render_template, url_for, flash
from app.forms import Permission
from app.middlewares.auth.login import user_login_require
from app.middlewares.auth.permissions import permission_require


@user_login_require
@permission_require(['permission.index'])
def admin_permission():
    data = db.session.query(model.Permission.id, model.Permission.name)
    return render_template('panel/permission/admin_permission.html', data=data)


@user_login_require
@permission_require(['permission.store'])
def permission_store():
    form = Permission()
    return render_template('panel/permission/permission_create.html', form=form,
                           tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
@permission_require(['permission.store'])
def permission_create():
    form = Permission()
    if form.validate:
        permission_check = db.session.query(model.Permission.name)\
            .filter_by(name=request.form['permission_name']).first()

        if permission_check:
            flash('Permission با این نام وجود دارد', 'error')
            return redirect(url_for('permission_store'))

        permission = model.Permission(
            name=request.form['permission_name']
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permission با موفقیت ایجاد شد', 'message')
        return redirect(url_for('admin_permission'))


@user_login_require
@permission_require(['permission.edit'])
def permission_edit(permission_id):
    permission = db.session.query(model.Permission.name).filter_by(id=permission_id).first()
    placeholders = {
        'permission_name': permission[0]
    }
    form = Permission(data=placeholders)
    return render_template('panel/permission/permission_edit.html', form=form, permission_id=permission_id,
                           tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
@permission_require(['permission.edit'])
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
            db.session.commit()
            flash('تغییرات با موفقیت انجام شد', 'message')
            return redirect(url_for('permission_edit', permission_id=permission_id))


@user_login_require
@permission_require(['permission.destroy'])
def permission_delete(permission_id):
    db.session.query(model.Permission).filter_by(id=permission_id).delete()
    db.session.commit()
    flash('permission با موفقیت حذف شد', 'message')
    return redirect(url_for('admin_permission'))
