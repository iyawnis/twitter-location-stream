from sqlalchemy import Column, BigInteger, JSON, Integer, String, Table, Text, DateTime
from database import Base, db_session, update_session
from datetime import datetime, timedelta

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(BigInteger, primary_key=True)
    tweet_text = Column(String(300), nullable=False)
    user_id = Column(String(50), nullable=False, index=True)
    coordinates = Column(String(100), nullable=True)
    created_at = Column(String(100), nullable=False)
    place = Column(String(100), nullable=False)
    retweet_count = Column(Integer, nullable=True)
    favorite_count = Column(Integer, nullable=True)
    reply_count = Column(Integer, nullable=False, default=0)
    last_update = Column(DateTime, nullable=True, index=True)
    json = Column(JSON, nullable=True)

    @classmethod
    def batch_to_update(cls):
        update_interval = datetime.now() - timedelta(hours=12)
        # Get the last 100 tweets that were updated more than *12 hours* ago, starting from oldest
        return (Tweet.query
            .filter(Tweet.last_update <= update_interval)
            .order_by(Tweet.last_update.asc())
            .limit(100))

    @classmethod
    def fetch_distinct_users(cls):
        return Tweet.query.distinct(Tweet.user_id)

    @classmethod
    def update_data(cls, tweet_id, tweet):
        """
        Store the latest Tweet data as returned from the API
        """
        db_session.query(Tweet).filter(Tweet.id == tweet_id).update({
            'favorite_count': tweet.favorite_count,
            'last_update': datetime.now(),
            'json': tweet._json,
            'retweet_count': tweet.retweet_count})
        db_session.commit()

    @classmethod
    def increment_replies(cls, tweet_id):
        """
        Increment the reply_count of the database Tweet matching tweet_id
        """
        (update_session
           .query(Tweet)
           .filter(Tweet.id == tweet_id)
           .update({'reply_count': Tweet.reply_count + 1}))

    @classmethod
    def bump_last_update(cls, tweet_id):
        """
        Mark a tweet as having been refreshed now
        """
        db_session.query(Tweet).filter(Tweet.id == tweet_id).update({
            'last_update': datetime.now()})
        db_session.commit()

    @classmethod
    def all_with_json(cls):
        """
        Retrieve all Tweets that have a value for their json field
        """
        return Tweet.query.filter(Tweet.json != None)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<Tweet {0}>'.format(self.id)

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    json = Column(JSON, nullable=True)
    follower_count = Column(Integer, nullable=False, default=0)
    last_update = Column(DateTime, nullable=True, index=True)

    @classmethod
    def update_data(cls, user_id, user_json):
        """
        Update the follower count for a user, and also the last_updated field
        """
        update_session.query(User).filter(User.id == str(user_id)).update({
            'json': user_json._json,
            'follower_count': user_json.followers_count,
            'last_update':datetime.now()
        })

    @classmethod
    def batch_create(cls, user_ids):
        """
        Batch create new user objects, from a list of user_ids
        This offers better performance compaired to individual create
        """
        update_session.bulk_save_objects([
            User(id=user_id)
            for user_id in user_ids
        ])

    @classmethod
    def fetch_users(cls):
        """
        Fetch all the users, ordered by the oldest updated first
        """
        return User.query.order_by(User.last_update.asc()).all()

    def __repr__(self):
        return '<User {0}>'.format(self.id)
