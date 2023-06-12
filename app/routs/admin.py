from flask import render_template, Blueprint, url_for, flash, redirect, request, make_response
from app import app, db, curs
from app.helpers.forms import Category, Product, User, ChangePassword
from wtforms.validators import DataRequired
import uuid, os, hashlib
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
        product_sql = 'SELECT product.id, product.name, product.quantity, product.price, product.discount, product.discount_date, category.name as category_name ' \
                      'FROM product ' \
                      'LEFT JOIN product_category on product.id = product_category.product_id ' \
                      'LEFT JOIN category on product_category.category_id = category.id ' \
                      'WHERE product.is_deleted IS NULL'
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
    elif menu_type == 'category':
        category_sql = 'SELECT A.id, A.name, A.description, A.image, B.name AS parent_name ' \
                       'FROM category A ' \
                       'LEFT JOIN category B ON B.id = A.parent_id ' \
                       'WHERE A.is_deleted IS NULL ' \
                       'ORDER BY A.id '
        curs.execute(category_sql)
        data = curs.fetchall()
    elif menu_type == 'information':
        information_sql = 'SELECT user.*, role.name AS role_name ' \
                          'FROM user ' \
                          'INNER JOIN user_role ON user.id = user_role.user_id ' \
                          'INNER JOIN role ON user_role.role_id = role.id ' \
                          'WHERE user.is_deleted IS NULL'
        curs.execute(information_sql)
        users = curs.fetchall()
        data = {}
        for user in users:
            if user['id'] not in data.keys():
                data[user['id']] = {
                    'name': f'{user["firstname"]} {user["lastname"]}',
                    'phone': user['phone'],
                    'email': user['email'],
                    'role': [user['role_name']]
                }
            else:
                data[user['id']]['role'].append(user['role_name'])
        print(data)
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

        create_category_sql = 'INSERT INTO category (name, description, image, parent_id) ' \
                              'VALUES (%s, %s, %s, %s)'
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

    category_sql = 'SELECT A.id, A.name, A.description, A.image, B.id AS parent ' \
                   'FROM category A ' \
                   'LEFT JOIN category B ON B.id = A.parent_id ' \
                   'WHERE A.id = %s ' \
                   'ORDER BY A.id'
    category_val = (category_id,)
    curs.execute(category_sql, category_val)
    category = curs.fetchone()
    print(category['name'])
    placeholders = {
        'category_name': category['name'],
        'category_parent': category['parent'],
        'category_description': category['description']
    }
    form = Category(request.form, data=placeholders)
    form.category_parent.choices = categories

    if request.method == 'POST':
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
        return redirect(url_for('admin.product_update', type='product'))

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
    product_delete_sql = 'UPDATE product ' \
                         'SET is_deleted = CURRENT_TIMESTAMP ' \
                         'WHERE id = %s'
    product_delete_val = (product_id,)
    curs.execute(product_delete_sql, product_delete_val)
    db.commit()
    return redirect(url_for('admin.administrator', type='product'))


@admin.route('/admin/user/create', methods=['GET', 'POST'])
def user_create():
    placeholders = {}
    if request.method == 'POST':
        check_user_sql = 'SELECT email ' \
                         'FROM user ' \
                         'WHERE email = %s'
        check_user_val = (request.form['email'],)
        curs.execute(check_user_sql, check_user_val)
        if curs.fetchone():
            flash('کاربر با این ایمیل قبلا ثبت شده', 'error')
        elif not request.form['role']:
            placeholders['firstname'] = request.form['firstname']
            placeholders['lastname'] = request.form['lastname']
            placeholders['phone'] = request.form['phone']
            placeholders['email'] = request.form['email']
            flash('یک رول برای کاربر تعیین کنید', 'error')
        else:
            user_password = request.form['password']
            user_password = user_password.encode()
            user_hashed_password = (hashlib.sha256(user_password)).hexdigest()

            user_create_sql = 'INSERT INTO user(firstname, lastname, email, phone, password) ' \
                              'VALUES (%s, %s, %s, %s, %s)'
            user_create_val = (request.form['firstname'], request.form['lastname'], request.form['email'],
                               request.form['phone'], user_hashed_password)
            curs.execute(user_create_sql, user_create_val)
            db.commit()
            user_role_sql = 'INSERT INTO user_role (user_id, role_id) ' \
                            'VALUES ((SELECT id FROM user WHERE email = %s), %s)'
            user_role_val = (request.form['email'], request.form['role'])
            curs.execute(user_role_sql, user_role_val)
            db.commit()
            flash('کاربر با موفقیت ایجاد شد', 'message')
            return redirect(url_for('admin.administrator', type='information'))
    form = User(request.form, data=placeholders)
    role_name_sql = 'SELECT id, name ' \
                    'FROM role'
    curs.execute(role_name_sql)
    role = [(None, 'Choose User Role ...')]
    for check in curs.fetchall():
        role.append((check['id'], check['name']))
    form.role.choices = role
    return render_template('user_create.html', form=form)


@admin.route('/admin/user/<int:user_id>/update', methods=['POST', 'GET'])
def user_update(user_id):
    if request.method == 'POST':
        user_update_sql = 'UPDATE user ' \
                          'set firstname=%s, lastname=%s, phone=%s, email=%s ' \
                          'WHERE id=%s'
        user_update_val = (request.form['firstname'], request.form['lastname'], request.form['phone'],
                           request.form['email'], user_id)
        curs.execute(user_update_sql, user_update_val)
        db.commit()
        role_update_sql = 'UPDATE user_role ' \
                          'SET role_id = %s ' \
                          'WHERE user_id = %s'
        role_update_val = (request.form['role'], user_id)
        curs.execute(role_update_sql, role_update_val)
        db.commit()
        flash('تغییرات با موفقیت انجام شد', 'message')
    user_sql = 'SELECT user.* ,role.id AS role ' \
               'FROM user ' \
               'INNER JOIN user_role ON user_role.user_id=user.id ' \
               'INNER JOIN role ON role.id=user_role.role_id ' \
               'WHERE user.id = %s'
    user_val = (user_id,)
    curs.execute(user_sql, user_val)
    user = curs.fetchone()
    placeholders = {
        'firstname': user['firstname'],
        'lastname': user['lastname'],
        'phone': user['phone'],
        'email': user['email'],
        'role': user['role']
    }
    form = User(request.form, data=placeholders)
    role_name_sql = 'SELECT id, name ' \
                    'FROM role'
    curs.execute(role_name_sql)
    role = [(0, 'Choose User Role ...')]
    for check in curs.fetchall():
        role.append((check['id'], check['name']))
    form.role.choices = role
    return render_template('user_update.html', form=form, user_id=user_id)


@admin.route('/admin/user/<int:user_id>/delete', methods=['POST', 'GET'])
def user_delete(user_id):
    user_delete_sql = 'UPDATE user ' \
                         'SET is_deleted = CURRENT_TIMESTAMP ' \
                         'WHERE id = %s'
    user_delete_val = (user_id,)
    curs.execute(user_delete_sql, user_delete_val)
    db.commit()
    return redirect(url_for('admin.administrator', type='information'))


@admin.route('/admin/user/<int:user_id>/password/update')
def user_password_update(user_id):
    if request.method == 'POST':
        password_check_sql = 'SELECT password ' \
                             'FROM user ' \
                             'WHERE id = %s'
        password_check_val = (user_id,)
        curs.execute(password_check_sql, password_check_val)
        user_password = request.form['password']
        user_password = user_password.encode()
        user_hashed_password = (hashlib.sha256(user_password)).hexdigest()
        if curs.fetchone() == user_hashed_password:
            flash('رمز عبور صحیح نیست', 'error')
        else:
            password_update_sql = 'UPDATE user ' \
                                  'SET password=%s ' \
                                  'WHERE id=%s'
            password_update_val = (user_hashed_password, user_id)
            curs.execute(password_update_sql, password_update_val)
            db.commit()
            return redirect(url_for('admin.user_update', type='information'))
    form = ChangePassword(request.form)
    return render_template('user_change_password.html', form=form)
