from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs
from app.helpers.forms import CreateCategory
import uuid
import os

admin = Blueprint('admin', __name__,
                  template_folder='templates',
                  static_folder='static'
                  )


@admin.route('/admin', methods=['GET', 'POST'])
def administrator():
    menu_type = request.args.get('type')
    form = None
    if menu_type == 'product':
        product_sql = 'SELECT * ' \
                      'FROM product'
        data = curs.execute(product_sql)
    elif menu_type == 'category':
        form = CreateCategory(request.form)

        if request.method == 'POST' and request.args.get('form_type') == 'create':
            category_check_sql = 'SELECT name ' \
                                 'FROM category ' \
                                 'WHERE name= %s'
            category_check_val = (request.form['category_name'],)
            curs.execute(category_check_sql, category_check_val)
            if curs.fetchone():
                flash('دسته بندی با نام وارد شده قبلا ایجاد شده است ...', 'error')
                return redirect(url_for('admin.administrator', type='category'))

            category_image = request.files['category_image']
            category_image_name = category_image.filename
            file_format = category_image_name[category_image_name.index('.'):]
            category_image_name = f'{str(uuid.uuid4())}{file_format}'
            category_image.save(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], category_image_name))

            create_category_sql = 'INSERT INTO category (name, description, image, active, parent_id) ' \
                                  'VALUES (%s, %s, %s, 1, (SELECT id FROM (SELECT id FROM category WHERE name=%s) as t))'
            create_category_val = (request.form['category_name'], request.form['category_description'], category_image_name, request.form['category_parent'])
            curs.execute(create_category_sql, create_category_val)
            db.commit()
            flash('دسته بندی با موفقیت ایجاد شد','message')


        category_name_sql = 'SELECT name ' \
                            'FROM category'
        curs.execute(category_name_sql)
        categories = [None]
        for i in curs.fetchall():
            categories.append(i['name'])
        form.category_parent.choices = categories

        category_sql = 'SELECT A.id, A.name, B.name AS parent_name, A.active ' \
                       'FROM category A ' \
                       'LEFT JOIN category B ON B.id = A.parent_id ' \
                       'ORDER BY A.id'
        curs.execute(category_sql)
        data = curs.fetchall()

    elif menu_type == 'information':
        information_sql = 'SELECT * ' \
                      'FROM information'
        data = curs.execute(information_sql)
    elif menu_type == 'role':
        role_sql = 'SELECT * ' \
                      'FROM role'
        data = curs.execute(role_sql)
    elif menu_type == 'permission':
        permission_sql = 'SELECT * ' \
                      'FROM permission'
        data = curs.execute(permission_sql)
    else:
        data = None

    return render_template('administrator.html', menu_type=menu_type, data=data, form=form)

