from sqlalchemy import Table, MetaData, JSON, Integer, Column
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    account = Table('tweet', meta, autoload=True)
    replyc = Column('reply_count', Integer, nullable=True)
    jsonc = Column('json', JSON, nullable=True)

    replyc.create(account)
    jsonc.create(account)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    account = Table('tweet', meta, autoload=True)
    account.c.json.drop()
    account.c.reply_count.drop()
