from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs

admin = Blueprint('admin', __name__,
                  template_folder='templates',
                  static_folder='static'
                  )


@admin.route('/admin')
def administrator():
    menu_type = request.args.get('type')
    if menu_type == 'product':
        product_sql = 'SELECT * ' \
                      'FROM product'
        curs.execute(product_sql)
    return render_template('administrator.html', menu_type=menu_type)

