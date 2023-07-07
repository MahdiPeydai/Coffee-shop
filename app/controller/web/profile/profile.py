from flask import request, render_template

from app.middlewares.auth.login import user_login_require


@user_login_require
def profile():
    return render_template('web/profile/profile.html', user_id=getattr(request, 'user_id', None))
