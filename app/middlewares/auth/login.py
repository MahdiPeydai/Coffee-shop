from flask import request, redirect, url_for, flash
from app import app
import jwt
from functools import wraps


def user_login_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'user_token' in request.cookies:
            token = request.cookies.get('user_token')
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = user_id['user_id']
            request.user_id = user_id
            return func(user_id, *args, **kwargs)
        else:
            user_id = None
            return func(user_id, *args, **kwargs)
    return decorator


def user_login_require(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'user_token' in request.cookies:
            token = request.cookies.get('user_token')
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = user_id['user_id']
            request.user_id = user_id
            return func(user_id, *args, **kwargs)
        else:
            flash('ابتدا وارد حساب کاربری خود شوید', 'error')
            return redirect(url_for('user_login'))

    return decorator
