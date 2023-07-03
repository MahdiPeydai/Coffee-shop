from app import db, model
from sqlalchemy import and_


def category_child_delete(product_id, children):
    for child in children:
        delete_product_category = model.product_category_association.delete().filter(and_(
            model.product_category_association.c.category_id == child.id,
            model.product_category_association.c.product_id == product_id))
        db.session.execute(delete_product_category)
        db.session.commit()
        category = db.session.query(model.Category).get(child.id)
        children_list = category.children
        category_child_delete(product_id, children_list)
