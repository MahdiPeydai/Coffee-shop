import functools

from flask import request, redirect, url_for, flash
from app import app, curs, db
import jwt


def permission_require(permissions):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            # token = request.cookies.get('token')
            # user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # user_id = user_id['user_id']
            user_id = 1

            permissions_sql = 'select permission.name as permission_name ' \
                              'from user ' \
                              'inner join user_role on user.id = user_role.user_id ' \
                              'inner join role on user_role.role_id = role.id ' \
                              'inner join role_permission on role_permission.role_id = role.id ' \
                              'inner join permission on permission.id = role_permission.permission_id ' \
                              'where user.id = %s '
            permissions_val = (user_id,)
            curs.execute(permissions_sql, permissions_val)
            user_permissions_dict = curs.fetchall()
            user_permissions = []
            for check in user_permissions_dict:
                user_permissions.append(check['permission_name'])

            if not set(permissions).issubset(user_permissions):
                flash('شما اجازه دسترسی به این بخش را ندارید', 'error')
                return redirect(request.referrer)

            return function(*args, **kwargs)
        return wrapper
    return decorator
