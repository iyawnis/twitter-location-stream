from sqlalchemy import Table, MetaData, Index

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    tweet = Table('tweet', meta, autoload=True)
    user_id_idx = Index('user_idx', tweet.c.user_id)
    user_id_idx.create(migrate_engine)

def downgrade(migrate_engine):
    tweet = Table('tweet', meta, autoload=True)
    user_id_idx = Index('user_idx', tweet.c.user_id)
    user_id_idx.drop(migrate_engine)