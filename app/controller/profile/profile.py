from flask import render_template

from app.controller.middlewares.auth.login import user_login_check


@user_login_check
def profile(user_id):
    return render_template('profile/profile.html', user_id=user_id)
