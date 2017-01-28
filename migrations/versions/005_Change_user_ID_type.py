from sqlalchemy import Table, MetaData, JSON, String, Column
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    user = Table('users', meta, autoload=True)
    user_id = Column('id', String, primary_key=True)
    user.c.id.alter(user_id)

def downgrade(migrate_engine):
    pass
