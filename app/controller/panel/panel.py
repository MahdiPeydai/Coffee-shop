from flask import render_template
from app.middlewares.auth.login import user_login_require
from app.middlewares.auth.permissions import permission_require


@user_login_require
@permission_require(['panel.index'])
def panel():
    return render_template('panel/panel.html')
