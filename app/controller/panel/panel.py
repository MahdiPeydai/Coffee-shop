from flask import render_template
from app.controller.middlewares.auth.login import admin_login_require


@admin_login_require
def panel():
    return render_template('panel/panel.html')
