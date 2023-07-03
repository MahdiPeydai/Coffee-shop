from app import app, db, model
from sqlalchemy import and_
from flask import request, redirect, render_template, url_for, flash
from app.forms import Role
from app.middlewares.auth.login import user_login_require
from app.middlewares.auth.permissions import permission_require


@user_login_require
@permission_require(['role.index'])
def admin_role(user_id):
    roles = db.session.query(model.Role.id, model.Role.name, model.Permission.name.label('permission')) \
        .join(model.role_permission_association, model.Role.id == model.role_permission_association.c.role_id,
              isouter=True) \
        .join(model.Permission, model.role_permission_association.c.permission_id == model.Permission.id, isouter=True)\
        .order_by(model.Role.id).all()
    data = {}
    for id, name, permission in roles:
        if id not in data.keys():
            data[id] = {
                'name': name,
                'permission': [permission]
            }
        else:
            data[id]['permission'].append(permission)
    return render_template('panel/role/admin_role.html', data=data)


@user_login_require
@permission_require(['role.store'])
def role_store(user_id):
    form = Role()

    permissions = db.session.query(model.Permission.id, model.Permission.name)
    permissions_list = []
    for id, name in permissions:
        permissions_list.append((str(id), name))
    form.role_permission.choices = permissions_list

    return render_template('panel/role/role_store.html', form=form, tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
@permission_require(['role.store'])
def role_create(user_id):
    form = Role()
    permissions = db.session.query(model.Permission.id, model.Permission.name)
    permissions_list = []
    for id, name in permissions:
        permissions_list.append((str(id), name))
    form.role_permission.choices = permissions_list
    if form.validate:
        role_check = db.session.query(model.Role).filter_by(name=request.form['role_name']).first()
        if role_check:
            flash('role با این نام قبلا ثبت شده', 'error')
            return redirect(url_for('role_store'))

        new_role = model.Role(
            name=request.form['role_name']
        )
        db.session.add(new_role)
        db.session.commit()
        new_role_id = new_role.id

        role_permission_str = request.form.getlist('role_permission')
        role_permission = []
        for i in role_permission_str:
            role_permission.append(int(i))

        for permission_id in role_permission:
            insert_query = model.role_permission_association.insert().values(role_id=new_role_id,
                                                                             permission_id=permission_id)
            db.session.execute(insert_query)
            db.session.commit()
        flash('Role با موفقیت ایجاد شد', 'message')
        return redirect(url_for('admin_role'))


@user_login_require
@permission_require(['role.edit'])
def role_edit(user_id, role_id):
    role_tuples = db.session.query(model.Role.name, model.Permission.id.label('permission')) \
        .join(model.role_permission_association, model.Role.id == model.role_permission_association.c.role_id,
              isouter=True) \
        .join(model.Permission, model.role_permission_association.c.permission_id == model.Permission.id, isouter=True) \
        .filter(model.Role.id == role_id)

    role = {}
    for name, permission in role_tuples:
        if not role.keys():
            role = {
                'role_name': name,
                'role_permission': [str(permission)]
            }
        else:
            role['role_permission'].append(str(permission))

    placeholders = {
        'role_name': role['role_name']
    }

    role_permission = []
    for permission_id in role['role_permission']:
        role_permission.append(permission_id)
    form = Role(data=placeholders)

    permissions = db.session.query(model.Permission.id, model.Permission.name)
    permissions_list = []
    for id, name in permissions:
        permissions_list.append((str(id), name))
    form.role_permission.choices = permissions_list
    form.role_permission.data = role_permission
    return render_template('panel/role/role_edit.html', form=form, role_id=role_id,
                           tinymce_key=app.config['TINYMCE_API_KEY'])


@user_login_require
@permission_require(['role.edit'])
def role_update(user_id, role_id):
    form = Role()

    permissions = db.session.query(model.Permission.id, model.Permission.name)
    permissions_list = []
    for id, name in permissions:
        permissions_list.append((str(id), name))
    form.role_permission.choices = permissions_list

    if form.validate:
        if request.form.get('_method') == 'PUT':
            role_check = db.session.query(model.Role).filter(and_(model.Role.name == request.form['role_name'],
                                                                  model.Role.id != role_id)).first()
            if role_check:
                flash('role با این نام قبلا ثبت شده', 'error')
                return redirect(url_for('panel.role_update'))
            else:
                role = db.session.query(model.Role).get(role_id)
                role.name = request.form['role_name']
                db.session.commit()
                old_permission_tuple = db.session.query(model.Permission.id) \
                    .join(model.role_permission_association,
                          model.role_permission_association.c.permission_id == model.Permission.id) \
                    .join(model.Role, model.Role.id == model.role_permission_association.c.role_id) \
                    .filter(model.Role.id == role_id)
                old_permission = []
                for id, in old_permission_tuple:
                    old_permission.append(id)
                new_permission_str = request.form.getlist('role_permission')
                new_permission = []
                for check in new_permission_str:
                    new_permission.append(int(check))
                for overplus in old_permission:
                    if overplus not in new_permission:
                        delete_query = model.role_permission_association.delete().filter(and_(
                            model.role_permission_association.c.role_id == role_id,
                            model.role_permission_association.c.permission_id == overplus
                        ))
                        db.session.execute(delete_query)
                        db.session.commit()
                for shortage in new_permission:
                    if shortage not in old_permission:
                        insert_query = model.role_permission_association.insert().values(
                            role_id=role_id,
                            permission_id=shortage
                        )
                        db.session.execute(insert_query)
                        db.session.commit()
                flash('تغییرات با موفقیت انجام شد', 'message')
                return redirect(url_for('role_edit', role_id=role_id))


@user_login_require
@permission_require(['role.destroy'])
def role_delete(user_id, role_id):
    db.session.query(model.Role).filter_by(id=role_id).delete()
    db.session.commit()
    flash('role با موفقیت حذف شد', 'message')
    return redirect(url_for('admin_role'))
