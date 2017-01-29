"""Edit the user table

Revision ID: c4d0a68a61d1
Revises: 1ce8c1d79314
Create Date: 2017-01-29 22:37:28.190215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4d0a68a61d1'
down_revision = '1ce8c1d79314'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('json', sa.JSON, nullable=True))
    op.drop_column('users', 'followers')


def downgrade():
    op.drop_column('users', 'json')
    op.add_column('users', sa.Column('followers', sa.JSON, nullable=True))
