from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs

home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static'
                 )


@home.route('/')
@home.route('/home')
@home.route('/index')
def home_page():
    slideshow_img_sql = 'SELECT image, destination ' \
                        'FROM slideshow ' \
                        'WHERE active = 1'
    curs.execute(slideshow_img_sql)
    slideshow_img = curs.fetchall()
    print(slideshow_img)

    return render_template('home.html', slideshow_img=slideshow_img)
