from sqlalchemy import Table, Column, JSON, Integer, BigInteger, MetaData

meta = MetaData()

users = Table(
    'users', meta,
    Column('id', BigInteger, primary_key=True),
    Column('followers', JSON),
    Column('follower_count', Integer, default=0)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()