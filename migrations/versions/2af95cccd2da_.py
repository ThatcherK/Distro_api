"""empty message

Revision ID: 2af95cccd2da
Revises: a8381c0a734b
Create Date: 2020-12-30 17:26:14.442357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2af95cccd2da'
down_revision = 'a8381c0a734b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory', 'quantity')
    # ### end Alembic commands ###
