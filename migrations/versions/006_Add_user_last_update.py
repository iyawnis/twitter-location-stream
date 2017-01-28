from sqlalchemy import Table, MetaData, DateTime, Column, Index
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('users', meta, autoload=True)
    last_update_c = Column('last_update', DateTime, nullable=True)
    last_update_c.create(user)
    last_update_idx = Index('last_update_idx', user.c.last_update)
    last_update_idx.create(migrate_engine)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('users', meta, autoload=True)
    last_update_idx = Index('last_update_idx', user.c.last_update)
    last_update_idx.drop(migrate_engine)
    user.c.last_update.drop()