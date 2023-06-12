from wtforms import Form, StringField, PasswordField, DateTimeLocalField, FileField, TextAreaField, SelectField, \
    SelectMultipleField, DateField, IntegerField, widgets, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileSize, FileAllowed, FileRequired
from app import app, curs


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Profile(Form):
    firstname = StringField('نام',
                            validators=[DataRequired(),
                                        Length(max=50)])
    lastname = StringField('نام خانوادگی',
                           validators=[DataRequired(),
                                       Length(max=50)])
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


class Category(Form):
    category_name = StringField('نام',
                                validators=[DataRequired(),
                                            Length(max=50)])
    category_description = TextAreaField('توضیحات',
                                         validators=[Length(max=255)])
    category_parent = SelectField('دسته بندی مادر')
    category_image = FileField('تصویر',
                               validators=[FileSize(max_size=1),
                                           FileAllowed(app.config['IMAGE_EXTENSION'])])


class Product(Form):
    product_name = StringField('نام',
                               validators=[DataRequired(),
                                           Length(max=50)])
    product_category = MultiCheckboxField('دسته بندی',
                                          choices=[])
    product_quantity = IntegerField('تعداد',
                                    validators=[DataRequired()])
    product_price = StringField('قیمت',
                                validators=[DataRequired(),
                                            Length(max=50)])
    product_discount = StringField('تخفیف',
                                   validators=[NumberRange(min=0, max=100)], )
    product_discount_date = DateTimeLocalField('تاریخ تخفیف',
                                               format='%Y-%m-%d %H:%M:%S')
    product_short_description = TextAreaField('توضیحات',
                                              validators=[Length(max=255)])


class User(Form):
    firstname = StringField('نام',
                            validators=[DataRequired(),
                                        Length(max=50)],
                            render_kw={"placeholder": "نام"})
    lastname = StringField('نام خانوادگی',
                           validators=[DataRequired(),
                                       Length(max=50)],
                           render_kw={"placeholder": "نام خانوادگی"})
    email = StringField('ایمیل',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)],
                        render_kw={"placeholder": "ایمیل"})
    phone = StringField('تلفن',
                        validators=[DataRequired(),
                                    Length(min=11, max=14, message='صحیح : "09** *** ****"')],
                        render_kw={"placeholder": "09** *** ****"})
    password = PasswordField('رمز عبور',
                             validators=[DataRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField('تکرار رمز عبور',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match!')])
    role = SelectField('Role')
