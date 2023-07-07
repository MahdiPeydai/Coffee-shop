from flask import request, render_template

from app import db, model
from sqlalchemy import and_

from app.middlewares.cart.cart import cart_check
from app.middlewares.auth.login import user_login_check

from app.controller.utils.cart_items_counter import cart_items_counter


@user_login_check
@cart_check
def product(product_id):
    cart_items_number = cart_items_counter()
    cart_id = getattr(request, 'cart_id', None)
    product = model.Product.query.filter_by(id=product_id).first()
    if product.discount:
        final_price = int(
            product.price * ((100 - product.discount) / 100))
    else:
        final_price = product.price
    product_information = {
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'price': product.price,
        'discount': product.discount,
        'final_price': final_price
    }

    cart = model.CartItem.query.filter(and_(model.CartItem.cart_id == cart_id, model.CartItem.product_id == product.id)).first()
    if cart:
        item_quantity = cart.quantity
    else:
        item_quantity = None
    if product.quantity < 10:
        limit = True
    else:
        limit = False

    categories = product.categories
    related_products_list = set()
    for category in categories:
        category_products = db.session.query(model.Product).join(model.product_category_association).filter(
            and_(model.product_category_association.c.category_id == category.id, model.Product.is_deleted.is_(None))
        ).all()
        for related_product in category_products:
            if related_product.id != product_id:
                related_products_list.add(related_product)

    related_products = []
    for related_product in related_products_list:
        if related_product.discount:
            final_price = int(
                related_product.price * ((100 - related_product.discount) / 100))
        else:
            final_price = related_product.price

        related_products.append({
            'id': related_product.id,
            'name': related_product.name,
            'quantity': related_product.quantity,
            'price': related_product.price,
            'discount': related_product.discount,
            'final_price': final_price
        })

    return render_template('web/product/product.html', user_id=getattr(request, 'user_id', None),
                           cart_items_number=cart_items_number, product=product_information,
                           item_quantity=item_quantity, limit=limit, related_products=related_products)
