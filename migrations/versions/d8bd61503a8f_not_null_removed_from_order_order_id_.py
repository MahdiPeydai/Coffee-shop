"""NOT NULL removed from order.order_id and order_product_id

Revision ID: d8bd61503a8f
Revises: a08d46f473a6
Create Date: 2023-07-08 03:10:56.983272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd8bd61503a8f'
down_revision = 'a08d46f473a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('product_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.alter_column('product_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('order_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
