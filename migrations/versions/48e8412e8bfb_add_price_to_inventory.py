"""Add price to inventory

Revision ID: 48e8412e8bfb
Revises: 0072043823ee
Create Date: 2021-01-04 09:13:42.427739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48e8412e8bfb'
down_revision = '0072043823ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('businesses', sa.Column('business_owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'businesses', 'users', ['business_owner_id'], ['id'])
    op.add_column('inventory', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('inventory', 'price')
    op.drop_constraint(None, 'businesses', type_='foreignkey')
    op.drop_column('businesses', 'business_owner_id')
    # ### end Alembic commands ###