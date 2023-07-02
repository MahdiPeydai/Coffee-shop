from app.model import db
from app.model.product import product_category_association


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    children = db.relationship("Category", backref=db.backref('parent', remote_side=[id]))

    products = db.relationship('Product', secondary=product_category_association,
                               backref=db.backref('category', lazy='dynamic'))
