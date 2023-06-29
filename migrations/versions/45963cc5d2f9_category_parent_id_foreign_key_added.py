"""category parent_id foreign-key added

Revision ID: 45963cc5d2f9
Revises: 52c1dd975085
Create Date: 2023-06-28 22:16:04.972580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45963cc5d2f9'
down_revision = '52c1dd975085'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'category', ['parent_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
