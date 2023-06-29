import functools

from flask import request, redirect, flash
from app import app, db, model
import jwt


def permission_require(permissions):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            token = request.cookies.get('admin_token')
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = user_id['user_id']

            # permissions_sql = 'select permission.name as permission_name ' \
            #                   'from user ' \
            #                   'inner join user_role on user.id = user_role.user_id ' \
            #                   'inner join role on user_role.role_id = role.id ' \
            #                   'inner join role_permission on role_permission.role_id = role.id ' \
            #                   'inner join permission on permission.id = role_permission.permission_id ' \
            #                   'where user.id = %s '
            # permissions_val = (user_id,)
            # curs.execute(permissions_sql, permissions_val)
            # user_permissions_dict = curs.fetchall()

            permission_name = db.session.query(model.Permission.name).\
                join(model.role_permission_association, model.Permission.id == model.role_permission_association.c.permission_id).\
                join(model.Role, model.Role.id == model.role_permission_association.c.role_id).\
                join(model.user_role_association, model.Role.id == model.user_role_association.c.role_id).\
                join(model.User, model.User.id == model.user_role_association.c.user_id).\
                filter(model.User.id == user_id)
            db.session.close()

            user_permissions = []
            for permission in permission_name:
                user_permissions.append(permission[0])
            # for check in user_permissions_dict:
            #     user_permissions.append(check['permission_name'])
            #
            if not set(permissions).issubset(user_permissions):
                flash('شما اجازه دسترسی به این بخش را ندارید', 'error')
                return redirect(request.referrer)

            return function(*args, **kwargs)
        return wrapper
    return decorator
