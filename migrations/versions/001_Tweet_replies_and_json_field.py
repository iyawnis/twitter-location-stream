from sqlalchemy import Table, MetaData, JSON, Integer, Column
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tweet = Table('tweet', meta, autoload=True)
    replyc = Column('reply_count', Integer, nullable=True)
    jsonc = Column('json', JSON, nullable=True)

    replyc.create(tweet)
    jsonc.create(tweet)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    tweet = Table('tweet', meta, autoload=True)
    tweet.c.json.drop()
    tweet.c.reply_count.drop()
