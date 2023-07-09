from app import db, model


def test():
    order = model.Order.query.filter_by(user_id=1).first()
    y = order.payment
    x = y[-1].transactions
    print(x)
    return f'{x}'
