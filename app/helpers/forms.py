from wtforms import Form, StringField, PasswordField, DateField, FileField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileSize, FileAllowed, FileRequired
from app import app


class Profile(Form):
    firstname = StringField('نام',
                            validators=[DataRequired(),
                                        Length(max=16)])
    lastname = StringField('نام خانوادگی',
                           validators=[DataRequired(),
                                       Length(max=16)])
    email = StringField('ایمیل',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)])
    phone = StringField('شماره همراه',
                        validators=[DataRequired(),
                                    Length(min=11, max=11, message='Correct Format : "09** *** ****"')])


class ChangePassword(Form):
    old_password = PasswordField('رمز عبور قدیمی',
                                 validators=[DataRequired(),
                                             Length(min=8,
                                                    message='Password should be at least %(min)d characters long')],
                                 render_kw={"placeholder": "رمز عبور قدیمی"})
    password = PasswordField('رمز عبور جدید',
                             validators=[DataRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')],
                             render_kw={"placeholder": "رمز عبور جدید"})
    confirm_password = PasswordField('تکرار رمز عبور جدید',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match!')],
                                     render_kw={"placeholder": "تکرار رمز عبور جدید"})
