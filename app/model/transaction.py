from app.model import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authority = db.Column(db.String(256))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    status = db.Column(db.String(10), server_default='pending')
    details = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    payment = db.relationship('Payment', backref=db.backref('transactions'))
