from app.model import db


class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    address_line = db.Column(db.String(400), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    transferee = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(14), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    is_deleted = db.Column(db.DateTime, default=None)

    orders = db.relationship('Order', backref=db.backref('address'))
