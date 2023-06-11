from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs
from app.helpers.forms import Category, Product
from wtforms.validators import DataRequired
import uuid
import os
import datetime

admin = Blueprint('admin', __name__,
                  template_folder='templates',
                  static_folder='static'
                  )


@admin.route('/admin', methods=['GET', 'POST'])
def administrator():
    menu_type = request.args.get('type')
    form = None
    if menu_type == 'product':
        form = Product(request.form)
        if request.method == 'POST' and request.args.get('form_type') == 'create':
            product_category_str = request.form.getlist('product_category')
            product_category = []
            for i in product_category_str:
                product_category.append(int(i))
            print(request.form)
            if request.form['product_discount_date'] == '':
                product_discount_date = None
            else:
                product_discount_date = request.form['product_discount_date']
            create_product_sql = 'INSERT INTO product (name, price, quantity, discount, discount_date, short_description) ' \
                                 'VALUES (%s, %s, %s, %s, %s, %s) '
            create_product_val = (request.form['product_name'], request.form['product_price'],
                                  request.form['product_quantity'], request.form['product_discount'],
                                  product_discount_date, request.form['product_short_description'])
            curs.execute(create_product_sql, create_product_val)
            db.commit()
            product_id_sql = 'SELECT id ' \
                             'FROM product ' \
                             'WHERE name = %s'
            product_id_val = (request.form['product_name'],)
            curs.execute(product_id_sql, product_id_val)
            product_id = curs.fetchone()['id']
            for category_id in product_category:
                product_category_sql = 'INSERT INTO product_category(product_id, category_id) ' \
                                       'VALUES (%s, %s)'
                product_category_val = (product_id, category_id)
                curs.execute(product_category_sql, product_category_val)
                db.commit()
            flash('محصول با موفقیت اضافه شد', 'message')

        product_sql = 'SELECT product.id, product.name, product.quantity, product.price, product.discount, product.discount_date, category.name as category_name ' \
                      'FROM product ' \
                      'LEFT JOIN product_category on product.id = product_category.product_id ' \
                      'LEFT JOIN category on product_category.category_id = category.id'
        curs.execute(product_sql)
        products = curs.fetchall()
        data = {}
        for product in products:
            if product['id'] not in data.keys():
                data[product['id']] = {
                    'name': product['name'],
                    'quantity': product['quantity'],
                    'price': product['price'],
                    'discount': product['discount'],
                    'discount_date': product['discount_date'],
                    'category': [product['category_name']]
                }
            else:
                data[product['id']]['category'].append(product['category_name'])
        category_name_sql = 'SELECT id, name ' \
                            'FROM category'
        curs.execute(category_name_sql)
        categories = []
        for category in curs.fetchall():
            categories.append((category['id'], category['name']))
        form.product_category.choices = categories
    elif menu_type == 'category':
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


@admin.route('/admin/category/create', methods=['GET', 'POST'])
def category_create():
    if request.method == 'POST':
        category_check_sql = 'SELECT name ' \
                             'FROM category ' \
                             'WHERE name= %s'
        category_check_val = (request.form['category_name'],)
        curs.execute(category_check_sql, category_check_val)
        if curs.fetchone():
            flash('دسته بندی با نام وارد شده قبلا ایجاد شده است ...', 'error')
            return redirect(url_for('admin.category_create'))

        category_image = request.files['category_image']
        category_image_name = category_image.filename
        file_format = category_image_name[category_image_name.index('.'):]
        category_image_name = f'{str(uuid.uuid4())}{file_format}'
        category_image.save(os.path.join(app.config['CATEGORY_IMAGE_FOLDER'], category_image_name))

        create_category_sql = 'INSERT INTO category (name, description, image, active, parent_id) ' \
                              'VALUES (%s, %s, %s, 1, %s)'
        create_category_val = (
            request.form['category_name'], request.form['category_description'], category_image_name,
            request.form['category_parent'])
        curs.execute(create_category_sql, create_category_val)
        db.commit()
        flash('دسته بندی با موفقیت ایجاد شد', 'message')
        return redirect(url_for('admin.administrator', type='category'))
    form = Category(request.form)
    form.category_image.validators.append(DataRequired())
    category_name_sql = 'SELECT id, name ' \
                        'FROM category'
    curs.execute(category_name_sql)
    categories = [(0, '')]
    for category in curs.fetchall():
        categories.append((category['id'], category['name']))
    form.category_parent.choices = categories
    return render_template('category_create.html', form=form)


@admin.route('/admin/category/<int:category_id>/update', methods=['GET', 'POST'])
def category_update(category_id):
    category_name_sql = 'SELECT id, name ' \
                        'FROM category'
    curs.execute(category_name_sql)
    categories = [(0, '')]
    for category in curs.fetchall():
        categories.append((category['id'], category['name']))

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
    form = Category(request.form, data=placeholders)
    form.category_parent.choices = categories

    if request.method == 'POST' and form.validate():
        if request.form['category_active'] == 'فعال':
            category_active = 1
        else:
            category_active = 0

        category_update_sql = 'UPDATE category ' \
                              'SET name=%s, parent_id=%s, description=%s, active=%s ' \
                              'WHERE id=%s'
        category_update_val = (
            request.form['category_name'], request.form['category_parent'], request.form['category_description'],
            category_active,
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
        return redirect(url_for('admin.administrator', type='category'))
    return render_template('category_update.html', form=form, category_id=category_id)


@admin.route('/admin/category/<int:category_id>/delete')
def category_delete(category_id):
    category_delete_sql = 'DELETE FROM category ' \
                          'WHERE id = %s'
    category_delete_val = (category_id,)
    curs.execute(category_delete_sql, category_delete_val)
    db.commit()
    parent_delete_sql = 'UPDATE category ' \
                        'SET parent_id = NULL ' \
                        'WHERE parent_id = %s'
    parent_delete_val = (category_id,)
    curs.execute(parent_delete_sql, parent_delete_val)
    db.commit()
    product_category_delete_sql = 'DELETE FROM product_category ' \
                                  'WHERE category_id = %s'
    product_category_delete_val = (category_id,)
    curs.execute(product_category_delete_sql, product_category_delete_val)
    db.commit()
    flash('دسته بندی با موفقیت حذف شد', 'message')
    return redirect(url_for('admin.administrator', type='category'))


@admin.route('/admin/product/create', methods=['GET', 'POST'])
def product_create():
    if request.method == 'POST':
        product_check_sql = 'SELECT name ' \
                            'FROM product ' \
                            'WHERE name = %s'
        product_check_val = (request.form['product_name'],)
        curs.execute(product_check_sql, product_check_val)
        if curs.fetchone():
            flash('محصول با نام وارد شده قبلا ایجاد شده است ...', 'error')
            return redirect(url_for('admin.product_create'))

        product_category_str = request.form.getlist('product_category')
        product_category = []
        for i in product_category_str:
            product_category.append(int(i))

        if request.form['product_discount_date'] == '':
            product_discount_date = None
        else:
            product_discount_date = request.form['product_discount_date']
        create_product_sql = 'INSERT INTO product (name, price, quantity, discount, discount_date, short_description) ' \
                             'VALUES (%s, %s, %s, %s, %s, %s) '
        create_product_val = (request.form['product_name'], request.form['product_price'],
                              request.form['product_quantity'], request.form['product_discount'],
                              product_discount_date, request.form['product_short_description'])
        curs.execute(create_product_sql, create_product_val)
        db.commit()
        product_id_sql = 'SELECT id ' \
                         'FROM product ' \
                         'WHERE name = %s'
        product_id_val = (request.form['product_name'],)
        curs.execute(product_id_sql, product_id_val)
        product_id = curs.fetchone()['id']
        for category_id in product_category:
            product_category_sql = 'INSERT INTO product_category(product_id, category_id) ' \
                                   'VALUES (%s, %s)'
            product_category_val = (product_id, category_id)
            curs.execute(product_category_sql, product_category_val)
            db.commit()
        flash('محصول با موفقیت اضافه شد', 'message')
        return redirect(url_for('admin.administrator', type='product'))
    form = Product(request.form)
    category_name_sql = 'SELECT id, name ' \
                        'FROM category'
    curs.execute(category_name_sql)
    categories = []
    for category in curs.fetchall():
        categories.append((category['id'], category['name']))
    form.product_category.choices = categories
    return render_template('product_create.html', form=form)


@admin.route('/admin/product/<int:product_id>/update', methods=['GET', 'POST'])
def product_update(product_id):
    if request.method == "POST":
        if request.form['product_discount_date'] == '':
            product_discount_date = None
        else:
            product_discount_date = request.form['product_discount_date']
        update_product_sql = 'UPDATE product ' \
                             'SET name=%s, price=%s, quantity=%s, discount=%s, discount_date=%s, short_description=%s ' \
                             'WHERE id=%s'
        update_product_val = (request.form['product_name'], request.form['product_price'],
                              request.form['product_quantity'], request.form['product_discount'],
                              product_discount_date, request.form['product_short_description'],
                              product_id)
        curs.execute(update_product_sql, update_product_val)
        db.commit()

        old_category_sql = 'SELECT category.id as category_id ' \
                           'FROM product ' \
                           'LEFT JOIN product_category on product.id = product_category.product_id ' \
                           'LEFT JOIN category on product_category.category_id = category.id ' \
                           'WHERE product.id=%s'
        old_category_val = (product_id,)
        curs.execute(old_category_sql, old_category_val)
        old_category_dict = curs.fetchall()
        old_category = []
        for check in old_category_dict:
            old_category.append(check['category_id'])
        new_category_str = request.form.getlist('product_category')
        new_category = []
        for check in new_category_str:
            new_category.append(int(check))

        for overplus in old_category:
            if overplus not in new_category:
                delete_category_sql = 'DELETE FROM product_category ' \
                                      'WHERE category_id=%s AND product_id=%s'
                delete_category_val = (overplus, product_id)
                curs.execute(delete_category_sql, delete_category_val)
                db.commit()
        for shortage in new_category:
            if shortage not in old_category:
                add_category_sql = 'INSERT INTO product_category (product_id, category_id)' \
                                   'VALUES (%s, %s)'
                add_category_val = (product_id, int(shortage))
                curs.execute(add_category_sql, add_category_val)
                db.commit()
        flash('تغییرات با موفقیت انجام شد', 'message')
        return redirect(url_for('admin.administrator', type='product'))

    product_sql = 'SELECT product.id, product.name, product.quantity, product.price, product.discount, product.discount_date, product.short_description, category.id as category_id ' \
                  'FROM product ' \
                  'LEFT JOIN product_category on product.id = product_category.product_id ' \
                  'LEFT JOIN category on product_category.category_id = category.id ' \
                  'WHERE product.id=%s'
    product_val = (product_id,)
    curs.execute(product_sql, product_val)
    products = curs.fetchall()
    product = {}
    for product_check in products:
        if product_check['id'] not in product.values():
            product = {
                'id': product_check['id'],
                'name': product_check['name'],
                'quantity': product_check['quantity'],
                'price': product_check['price'],
                'discount': product_check['discount'],
                'discount_date': product_check['discount_date'],
                'short_description': product_check['short_description'],
                'category': [product_check['category_id']]
            }
        else:
            product['category'].append(product_check['category_id'])
    placeholders = {
        'product_name': product['name'],
        'product_quantity': product['quantity'],
        'product_price': product['price'],
        'product_discount': product['discount'],
        'product_discount_date': product['discount_date'],
        'product_short_description': product['short_description']
    }
    form = Product(request.form, data=placeholders)
    category_name_sql = 'SELECT id, name ' \
                        'FROM category'
    curs.execute(category_name_sql)
    categories = []
    for category in curs.fetchall():
        categories.append((category['id'], category['name']))
    form.product_category.choices = categories
    product_category = []
    for category_id in product['category']:
        product_category.append(str(category_id))
    form.product_category.data = product_category

    return render_template('product_update.html', form=form, product_id=product_id)


@admin.route('/admin/product/<int:product_id>/delete')
def product_delete(product_id):
    product_delete_sql = 'DELETE FROM product ' \
                         'WHERE id = %s'
    product_delete_val = (product_id,)
    curs.execute(product_delete_sql, product_delete_val)
    db.commit()
    product_category_delete_sql = 'DELETE FROM product_category ' \
                                  'WHERE product_id = %s'
    product_category_delete_val = (product_id)
    curs.execute(product_category_delete_sql, product_category_delete_val)
    db.commit()
    return redirect(url_for('admin.administrator', type='product'))
