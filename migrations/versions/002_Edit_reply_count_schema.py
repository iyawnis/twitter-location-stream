from sqlalchemy import Table, MetaData, JSON, Integer, Column
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tweet = Table('tweet', meta, autoload=True)
    replyc = Column('reply_count', Integer, nullable=False, default=0)
    tweet.c.reply_count.alter(replyc)

def downgrade(migrate_engine):
    pass
