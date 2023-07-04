from app.model import db
from app.model.user_role import user_role_association
from app.model.role_permission import role_permission_association


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    permissions = db.relationship('Permission', secondary=role_permission_association,
                                  backref=db.backref('roles', lazy='dynamic'))
