from app.model import db


product_category_association = db.Table(
    'product_category',

    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False)
)