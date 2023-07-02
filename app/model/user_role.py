from app.model import db


user_role_association = db.Table(
    'user_role',

    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), nullable=False)
)
