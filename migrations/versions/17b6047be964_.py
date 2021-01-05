"""empty message

Revision ID: 17b6047be964
Revises: 48e8412e8bfb
Create Date: 2021-01-04 14:14:30.054274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b6047be964'
down_revision = '48e8412e8bfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('phone_number', sa.String(length=128), nullable=False))
    op.drop_column('customers', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customers', sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_column('customers', 'phone_number')
    # ### end Alembic commands ###