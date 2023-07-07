from flask import request, render_template

from app import db, model
from sqlalchemy import and_

from app.middlewares.auth.login import user_login_check
from app.middlewares.cart.cart import cart_check

from app.controller.utils.cart_items_counter import cart_items_counter
from app.controller.utils.category_dict_builder import build_categories_dict


@user_login_check
@cart_check
def category_all():
    cart_items_number = cart_items_counter()

    base_categories = db.session.query(model.Category).filter_by(parent_id=None).all()
    categories_list = build_categories_dict(base_categories)

    categories_data = {}
    categories = db.session.query(model.Category).all()
    for category in categories:
        categories_data[category.id] = {
                    'name': category.name,
                    'image': category.image
        }

    products = db.session.query(model.Product).filter_by(is_deleted=None).all()

    category_products = []
    for product in products:
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price
        category_products.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'discount': product.discount,
            'final_price': final_price
        })

    return render_template('web/category/category.html', user_id=getattr(request, 'user_id', None),
                           cart_items_number=cart_items_number, categories_list=categories_list,
                           categories_data=categories_data, category_products=category_products)


@user_login_check
@cart_check
def category(category_id):
    cart_items_number = cart_items_counter()

    base_categories = db.session.query(model.Category).filter_by(parent_id=None).all()
    categories_list = build_categories_dict(base_categories)

    categories_data = {}
    categories = db.session.query(model.Category).all()
    for category in categories:
        categories_data[category.id] = {
            'name': category.name,
            'image': category.image
        }

    products = db.session.query(model.Product)\
        .join(model.product_category_association, model.product_category_association.c.product_id == model.Product.id)\
        .join(model.Category, model.Category.id == model.product_category_association.c.category_id)\
        .filter(and_(model.Category.id == category_id, model.Product.is_deleted == None)).all()

    category_products = []
    for product in products:
        if product.discount:
            final_price = int(
                product.price * ((100 - product.discount) / 100))
        else:
            final_price = product.price
        category_products.append({
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'discount': product.discount,
            'final_price': final_price
        })



    return render_template('web/category/category.html', user_id=getattr(request, 'user_id', None),
                           cart_items_number=cart_items_number, categories_list=categories_list,
                           categories_data=categories_data, category_products=category_products)
