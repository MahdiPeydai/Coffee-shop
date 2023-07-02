from app.model import db


role_permission_association = db.Table(
    'role_permission',

    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id', ondelete="CASCADE"), nullable=False),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete="CASCADE"), nullable=False)
)