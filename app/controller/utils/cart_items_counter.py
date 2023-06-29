from app import db, model


def cart_items_counter(cart_id):
    cart_items = db.session.query(model.CartItem.quantity) \
        .filter(model.CartItem.cart_id == cart_id).all()
    items = 0
    for quantity, in cart_items:
        items += quantity

    return items
