from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs
from app.helpers.forms import CreateCategory, UpdateCategory
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
        product_sql = 'SELECT product.id, product.name, product.quantity, product.price, product.discount, product.discount_date, category.id as category_id' \
                      'FROM product ' \
                      'INNER JOIN product_category on product.id = product_category.product_id ' \
                      'INNER JOIN category on product_category.category_id = category.id'
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

            if request.form['category_parent'] == '':
                category_parent = 0
            else:
                parent_id_sql = 'SELECT id ' \
                                'FROM category ' \
                                'WHERE name=%s'
                parent_id_val = (request.form['category_parent'],)
                curs.execute(parent_id_sql, parent_id_val)
                category_parent = curs.fetchone()['id']

            create_category_sql = 'INSERT INTO category (name, description, image, active, parent_id) ' \
                                  'VALUES (%s, %s, %s, 1, %s)'
            create_category_val = (request.form['category_name'], request.form['category_description'], category_image_name, category_parent)
            curs.execute(create_category_sql, create_category_val)
            db.commit()
            flash('دسته بندی با موفقیت ایجاد شد', 'message')

        category_name_sql = 'SELECT name ' \
                            'FROM category'
        curs.execute(category_name_sql)
        categories = ['']
        for i in curs.fetchall():
            categories.append(i['name'])
        form.category_parent.choices = categories

        category_sql = 'SELECT A.id, A.name, A.description, A.image, B.name AS parent_name, A.active ' \
                       'FROM category A ' \
                       'LEFT JOIN category B ON B.id = A.parent_id ' \
                       'ORDER BY A.id'
        curs.execute(category_sql)
        data = curs.fetchall()
        for cat in data:
            cat['active'] = int.from_bytes(cat['active'], "big")
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


@admin.route('/admin/category/<int:category_id>/update', methods=['GET', 'POST'])
def category_update(category_id):
    if request.method == 'POST':
        if request.form['category_parent'] != '':
            parent_id_sql = 'SELECT id ' \
                            'FROM category ' \
                            'WHERE name=%s'
            parent_id_val = (request.form['category_parent'],)
            curs.execute(parent_id_sql, parent_id_val)
            parent_id = curs.fetchone()['id']
        else:
            parent_id = 0


        if request.form['category_active'] == 'فعال':
            category_active = 1
        else:
            category_active = 0


        category_update_sql = 'UPDATE category ' \
                              'SET name=%s, parent_id=%s, description=%s, active=%s ' \
                              'WHERE id=%s'
        category_update_val = (
            request.form['category_name'], parent_id, request.form['category_description'], category_active,
            category_id)
        curs.execute(category_update_sql, category_update_val)
        db.commit()
        if request.files['category_image']:
            old_category_image_sql = 'SELECT image ' \
                                     'FROM category ' \
                                     'WHERE id = %s'
            old_category_image_val = (category_id,)
            curs.execute(old_category_image_sql, old_category_image_val)
            old_img = curs.fetchone()['image']
            os.remove(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], old_img))

            category_image = request.files['category_image']
            category_image_name = category_image.filename
            file_format = category_image_name[category_image_name.index('.'):]
            category_image_name = f'{str(uuid.uuid4())}{file_format}'
            category_image.save(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], category_image_name))

            new_category_image_sql = 'UPDATE category ' \
                                     'SET image = %s ' \
                                     'WHERE id = %s'
            new_category_image_val = (category_image_name, category_id)
            curs.execute(new_category_image_sql, new_category_image_val)
            db.commit()
        flash('نغییرات با موفقیت انجام شد', 'message')
        return redirect(url_for('admin.administrator', type='category', category_id=category_id))

    category_name_sql = 'SELECT name ' \
                        'FROM category'
    curs.execute(category_name_sql)
    categories = [None]
    for i in curs.fetchall():
        categories.append(i['name'])

    category_sql = 'SELECT A.id, A.name, A.description, A.image, B.name AS parent_name, A.active ' \
                   'FROM category A ' \
                   'LEFT JOIN category B ON B.id = A.parent_id ' \
                   'WHERE A.id = %s ' \
                   'ORDER BY A.id'
    category_val = (category_id,)
    curs.execute(category_sql, category_val)
    category = curs.fetchone()
    category['active'] = int.from_bytes(category['active'], "big")
    print(category['name'])
    placeholders = {
        'category_name': category['name'],
        'category_parent': category['parent_name'],
        'category_description': category['description']
    }
    if category['active'] == 0:
        placeholders['category_active'] = 'غیرفعال'
    form = UpdateCategory(request.form, data=placeholders)
    form.category_parent.choices = categories

    return render_template('category_update.html', form=form, category_id=category_id)
