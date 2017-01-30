"""Add new User fields

Revision ID: f25da7d345cc
Revises: c4d0a68a61d1
Create Date: 2017-01-30 18:32:53.592293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f25da7d345cc'
down_revision = 'c4d0a68a61d1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('follower_ids', sa.JSON, nullable=True))
    op.add_column('users', sa.Column('total_tweet_favourites', sa.Integer, nullable=False, server_default='0'))
    op.add_column('users', sa.Column('total_tweet_retweets', sa.Integer, nullable=False, server_default='0'))
    op.add_column('users', sa.Column('total_tweet_replies', sa.Integer, nullable=False, server_default='0'))

def downgrade():
    op.drop_column('users', 'follower_ids')
    op.drop_column('users', 'total_tweet_favourites')
    op.drop_column('users', 'total_tweet_retweets')
    op.drop_column('users', 'total_tweet_replies')
