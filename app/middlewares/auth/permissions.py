import functools

from flask import request, redirect, flash
from app import app, db, model
import jwt


def permission_require(permissions):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            token = request.cookies.get('user')
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = user_id['user_id']

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

            if not set(permissions).issubset(user_permissions):
                flash('شما اجازه دسترسی به این بخش را ندارید', 'error')
                return redirect(request.referrer)
            return function(*args, **kwargs)
        return wrapper
    return decorator
