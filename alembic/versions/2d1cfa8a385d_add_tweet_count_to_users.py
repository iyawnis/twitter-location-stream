"""Add tweet count to users

Revision ID: 2d1cfa8a385d
Revises: f25da7d345cc
Create Date: 2017-01-30 22:57:07.970483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d1cfa8a385d'
down_revision = 'f25da7d345cc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('tweet_count', sa.Integer, nullable=False, server_default='0'))


def downgrade():
    op.drop_column('users', 'tweet_count')
