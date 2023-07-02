from flask import render_template
from app.middlewares.auth.login import user_login_require


@user_login_require
def panel(user_id):
    return render_template('panel/panel.html')
