from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs
from app.helpers.forms import Profile, ChangePassword

profile = Blueprint('profile', __name__,
                    template_folder='templates',
                    static_folder='static'
                    )


@profile.route('/profile')
def main_profile():
    profile_form = Profile(request.form)
    change_password_form = ChangePassword(request.form)
    return render_template('profile.html', profile_form=profile_form, change_password_form=change_password_form)
