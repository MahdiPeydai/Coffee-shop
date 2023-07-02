from app.model import db
from app.model.user_role import user_role_association


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60))
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = db.Column(db.DateTime, default=None)

    addresses = db.relationship('Address', backref=db.backref('user'))
    roles = db.relationship('Role', secondary=user_role_association, backref=db.backref('user', lazy='dynamic'))
    carts = db.relationship('Cart', backref=db.backref('user'))
    orders = db.relationship('Order', backref=db.backref('user'))
