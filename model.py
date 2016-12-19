from sqlalchemy import Column, Integer, String, Table, Text, DateTime
from database import Base, db_session
from datetime import datetime, timedelta

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    tweet_text = Column(String(300), nullable=False)
    user_id = Column(String(50), nullable=False)
    coordinates = Column(String(100), nullable=True)
    created_at = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    retweet_count = Column(Integer, nullable=True)
    favorite_count = Column(Integer, nullable=True)
    last_update = Column(DateTime, nullable=True, index=True)

    @classmethod
    def batch_to_update(cls):
        update_interval = datetime.now() - timedelta(minutes=10)
        # Get the last 100 tweets that have not been updated within the interval, starting from oldest
        return (Tweet.query
            .filter(Tweet.last_update <= update_interval)
            .order_by(Tweet.last_update.asc())
            .limit(100))

    @classmethod
    def update_counts(cls, tweet_id, favorite_count, retweet_count):
        db_session.query(Tweet).filter(Tweet.id == tweet_id).update({
            'favorite_count': favorite_count,
            'last_update': datetime.now(),
            'retweet_count': retweet_count})
        db_session.commit()

    @classmethod
    def bump_last_update(cls, tweet_id):
        db_session.query(Tweet).filter(Tweet.id == tweet_id).update({
            'last_update': datetime.now()})
        db_session.commit()


    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<Tweet {0}>'.format(self.id)