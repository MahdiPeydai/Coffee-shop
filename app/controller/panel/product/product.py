from app import db, model
from sqlalchemy import and_, func
from flask import request, redirect, render_template, url_for, flash
from app.forms import Product
from app.middlewares.auth.login import user_login_require
from app.middlewares.auth.permissions import permission_require


@user_login_require
@permission_require(['product'])
def admin_product(user_id):
    products = db.session.query(model.Product.id, model.Product.name, model.Product.quantity,
                                model.Product.price, model.Product.discount, model.Category.name.label('category_name'))\
        .join(model.product_category_association, model.Product.id == model.product_category_association.c.product_id, isouter=True) \
        .join(model.Category, model.Category.id == model.product_category_association.c.category_id, isouter=True) \
        .filter(model.Product.is_deleted == None)
    db.session.commit()
    data = {}
    for id, name, quantity, price, discount, category_name in products:
        if id not in data.keys():
            data[id] = {
                'name': name,
                'quantity': quantity,
                'price': price,
                'discount': discount,
                'category': [category_name]
            }
        else:
            data[id]['category'].append(category_name)
    return render_template('panel/product/admin_product.html', data=data)


@user_login_require
@permission_require(['product', 'product_crud'])
def product_create(user_id):
    form = Product()

    category_query = db.session.query(model.Category.id, model.Category.name)
    db.session.close()
    categories = []
    for id, name in category_query:
        categories.append((id, name))
    form.product_category.choices = categories
    return render_template('panel/product/product_create.html', form=form)


@user_login_require
@permission_require(['product', 'product_crud'])
def product_store(user_id):
    form = Product()
    category_query = db.session.query(model.Category.id, model.Category.name)
    db.session.close()
    categories = []
    for id, name in category_query:
        categories.append((str(id), name))
    form.product_category.choices = categories
    if form.validate:
        product_check = db.session.query(model.Product.name).filter(and_(model.Product.name == request.form['product_name'],
                                                                         model.Product.is_deleted == None)).first()
        if product_check:
            flash('محصول با نام وارد شده وجود دارد ...', 'error')
            return redirect(url_for('product_create'))

        product_category_str = request.form.getlist('product_category')
        product_category = []
        for i in product_category_str:
            product_category.append(int(i))

        if request.form['product_discount']:
            product_discount = request.form['product_discount']
        else:
            product_discount = None

        new_product = model.Product(
            name=request.form['product_name'],
            price=int(request.form['product_price']),
            quantity=request.form['product_quantity'],
            discount=product_discount,
        )
        db.session.add(new_product)
        db.session.commit()
        product_id = new_product.id

        for category_id in product_category:
            product_category = model.product_category_association.insert().values(product_id=product_id,
                                                                                  category_id=category_id)
            db.session.execute(product_category)
            db.session.commit()
        flash('محصول با موفقیت اضافه شد', 'message')
        return redirect(url_for('admin_product'))


@user_login_require
@permission_require(['product', 'product_crud'])
def product_edit(user_id, product_id):
    products = db.session.query(model.Product.id, model.Product.name, model.Product.quantity, model.Product.price,
                                model.Product.discount, model.Category.id.label('category')) \
        .join(model.product_category_association, model.Product.id == model.product_category_association.c.product_id,
              isouter=True) \
        .join(model.Category, model.Category.id == model.product_category_association.c.category_id, isouter=True) \
        .filter(model.Product.id == product_id)

    product = {}
    for id, name, quantity, price, discount, category in products:
        if 'id' not in product.keys():
            product = {
                'id': id,
                'name': name,
                'quantity': quantity,
                'price': price,
                'discount': discount,
                'category': [str(category)]
            }
        else:
            product['category'].append(str(category))
    placeholders = {
        'product_name': product['name'],
        'product_quantity': product['quantity'],
        'product_price': product['price'],
        'product_discount': product['discount']
    }
    form = Product(data=placeholders)
    category_query = db.session.query(model.Category.id, model.Category.name)
    db.session.close()
    categories = []
    for id, name in category_query:
        categories.append((id, name))
    form.product_category.choices = categories
    form.product_category.data = product['category']
    return render_template('panel/product/product_edit.html', form=form, product_id=product_id)


@user_login_require
@permission_require(['product', 'product_crud'])
def product_update(user_id, product_id):
    form = Product()
    category_query = db.session.query(model.Category.id, model.Category.name)
    db.session.close()
    categories = []
    for id, name in category_query:
        categories.append((str(id), name))
    form.product_category.choices = categories
    if form.validate:
        if request.form.get('_method') == 'PUT':
            product_check = db.session.query(model.Product.name).filter(
                and_(model.Product.name == request.form['product_name'],
                     model.Product.is_deleted == None,
                     model.Product.id != product_id)).first()

            if product_check:
                flash('محصول با نام وارد شده وجود دارد ...', 'error')
                return redirect(url_for('product_edit', product_id=product_id))

            if request.form['product_discount']:
                product_discount = request.form['product_discount']
            else:
                product_discount = None

            product = db.session.query(model.Product).get(product_id)
            product.name = request.form['product_name']
            product.price = request.form['product_price']
            product.quantity = request.form['product_quantity']
            product.discount = product_discount
            db.session.commit()

            if len(request.form.getlist('product_category')) == 0:
                flash('محصول باید یک دسته‌بندی داشته باشد', 'error')
                return redirect(url_for('product_edit', product_id=product_id))

            old_category_tuple = db.session.query(model.Category.id) \
                .join(model.product_category_association, model.Category.id == model.product_category_association.c.category_id) \
                .join(model.Product, model.Product.id == model.product_category_association.c.product_id) \
                .filter(model.Product.id == product_id)
            old_category = []
            for id, in old_category_tuple:
                old_category.append(id)

            new_category_str = request.form.getlist('product_category')
            new_category = []
            for id in new_category_str:
                new_category.append(int(id))

            for overplus in old_category:
                if overplus not in new_category:
                    delete_product_category = model.product_category_association.delete().filter(
                        model.product_category_association.c.category_id == overplus
                    )
                    db.session.execute(delete_product_category)
                    db.session.commit()

            for shortage in new_category:
                if shortage not in old_category:
                    new_product_category = model.product_category_association.insert().values(
                        product_id=product_id,
                        category_id=int(shortage)
                    )
                    db.session.execute(new_product_category)
                    db.session.commit()
            flash('تغییرات با موفقیت انجام شد', 'message')
            return redirect(url_for('product_edit', product_id=product_id))


@user_login_require
@permission_require(['product', 'product_crud'])
def product_delete(user_id, product_id):
    product = db.session.query(model.Product).get(product_id)
    product.is_deleted = func.current_timestamp()

    db.session.commit()
    flash('محصول با موفقیت حذف شد ...', 'message')
    return redirect(url_for('admin_product'))
