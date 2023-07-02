from flask import render_template

from app import db, model

from app.middlewares.auth.login import user_login_require


@user_login_require
def user_order(user_id):
    order_tuple = db.session.query(model.Order.id, model.Order.created_at, model.Order.total, model.Product.name) \
        .join(model.OrderItem, model.Order.id == model.OrderItem.order_id) \
        .join(model.Product, model.OrderItem.product_id == model.Product.id) \
        .join(model.User, model.User.id == model.Order.user_id) \
        .filter(model.User.id == user_id).all()
    user_orders = {}
    for order in order_tuple:
        if order[0] not in user_orders.keys():
            user_orders[order[0]] = {
                'date': order[1],
                'total': order[2],
                'product': [order[3]]
            }
        else:
            user_orders[order[0]]['product'].append(order[3])
    return render_template('web/profile/order/order.html', user_orders=user_orders, user_id=user_id)
