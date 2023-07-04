from app.model import db
from app.model.product_category import product_category_association


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.SmallInteger, default=None)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = db.Column(db.DateTime, default=None)

    images = db.relationship('ProductImage', backref=db.backref('product'))
