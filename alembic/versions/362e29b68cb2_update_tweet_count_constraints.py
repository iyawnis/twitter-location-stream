"""Update Tweet count constraints

Revision ID: 362e29b68cb2
Revises: 2d1cfa8a385d
Create Date: 2017-02-01 18:38:03.000580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362e29b68cb2'
down_revision = '2d1cfa8a385d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('UPDATE tweet SET retweet_count=0 where retweet_count is null')
    op.execute('UPDATE tweet SET favorite_count=0 where favorite_count is null')
    op.execute('UPDATE tweet SET reply_count=0 where reply_count is null')

    op.alter_column('tweet', 'retweet_count', server_default='0', nullable=False)
    op.alter_column('tweet', 'favorite_count', server_default='0', nullable=False)
    op.alter_column('tweet', 'reply_count', server_default='0', nullable=False)


def downgrade():
    pass
