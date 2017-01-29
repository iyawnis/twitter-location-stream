"""Database V2

Revision ID: 1ce8c1d79314
Revises:
Create Date: 2017-01-29 16:08:04.349074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ce8c1d79314'
down_revision = None
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('followers', sa.JSON, nullable=True),
        sa.Column('follower_count', sa.Integer, server_default='0'),
        sa.Column('last_update', sa.DateTime, nullable=True),
    )
    op.create_index('last_update_idx', 'users', ['last_update'])


    op.add_column('tweet', sa.Column('reply_count', sa.Integer, nullable=False, server_default='0'))
    op.add_column('tweet', sa.Column('json', sa.JSON, nullable=True))
    op.create_index('user_id_idx', 'tweet', ['user_id'])


def downgrade():
    op.drop_table('users')
    op.drop_column('tweet', 'json')
    op.drop_column('tweet', 'reply_count')
    op.drop_index('last_update_idx', 'users')
    op.drop_index('user_id_idx', 'tweet')