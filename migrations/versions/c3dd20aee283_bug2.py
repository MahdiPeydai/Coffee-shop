"""bug2

Revision ID: c3dd20aee283
Revises: 1fcffea0c4a0
Create Date: 2023-06-25 15:43:29.205502

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c3dd20aee283'
down_revision = '1fcffea0c4a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_column('country')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country', mysql.VARCHAR(length=52), nullable=False))

    # ### end Alembic commands ###