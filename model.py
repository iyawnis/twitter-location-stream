from sqlalchemy import func,Column, BigInteger, JSON, Integer, String, Table, Text, DateTime
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
    retweet_count = Column(Integer, nullable=False, default=0, server_default='0')
    favorite_count = Column(Integer, nullable=False, default=0, server_default='0')
    reply_count = Column(Integer, nullable=False, default=0, server_default='0')
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
    def fetch_distinct_user_ids(cls):
        return [str(user_id[0]) for user_id in db_session.query(Tweet.user_id).distinct(Tweet.user_id)]

    @classmethod
    def get_user_tweet_counts(cls, user_id):
        return (db_session
            .query(
                func.sum(Tweet.favorite_count).label('favorite_count'),
                func.sum(Tweet.retweet_count).label('retweet_count'),
                func.sum(Tweet.reply_count).label('reply_count'),
                func.count(Tweet.id).label('tweet_count'))
            .filter(Tweet.user_id == user_id)
            .group_by(Tweet.user_id).first())

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
        return update_session.query(Tweet.id).filter(Tweet.json != None)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def __repr__(self):
        return '<Tweet {0}>'.format(self.id)

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    json = Column(JSON, nullable=True)
    follower_ids = Column(JSON, nullable=True)
    follower_count = Column(Integer, nullable=False, default=0, server_default='0')
    last_update = Column(DateTime, nullable=True, index=True)
    total_tweet_favourites = Column(Integer, nullable=False, default=0, server_default='0')
    tweet_count = Column(Integer, nullable=False, default=0)
    total_tweet_retweets = Column(Integer, nullable=False, default=0, server_default='0')
    total_tweet_replies = Column(Integer, nullable=False, default=0, server_default='0')

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
        db_session.bulk_insert_mappings(User, [
            dict(id=user_id)
            for user_id in user_ids
        ])
        db_session.commit()

    @classmethod
    def update_followers(cls, user_id, follower_ids):
        """
        Update the followers for the specified user
        """
        (update_session.query(User)
            .filter(User.id == user_id).update({
                'follower_ids': list(follower_ids),
                'follower_count': len(follower_ids),
                'last_update': datetime.now()
            }))

    @classmethod
    def update_user_counters(cls):
        aggregated = (update_session
            .query(
                User.id.label("id"),
                func.sum(Tweet.favorite_count).label("total_tweet_favourites"),
                func.sum(Tweet.retweet_count).label("total_tweet_retweets"),
                func.sum(Tweet.reply_count).label("total_tweet_replies"),
                func.count(Tweet.id).label("tweet_count"))
            .select_from(User)
            .join(Tweet, Tweet.user_id == User.id)
            .group_by(User.id)
            .subquery()
            .alias("aggregated"))
        query = (User.__table__
            .update()
            .values(
                total_tweet_favourites=aggregated.c.total_tweet_favourites,
                total_tweet_retweets=aggregated.c.total_tweet_retweets,
                total_tweet_replies=aggregated.c.total_tweet_replies,
                tweet_count=aggregated.c.tweet_count)
            .where(User.__table__.c.id == aggregated.c.id))
        update_session.execute(query)

    @classmethod
    def get_highest_counter_users(cls):
        """
        Get the top users, based on their tweets favourite and retweet counts
        """
        return (User.query
            .order_by(User.total_tweet_favourites.desc(),
                User.total_tweet_retweets.desc())
            .limit(100))

    @classmethod
    def save(cls):
        db_session.commit()

    @classmethod
    def fetch_user_ids(cls):
        """
        Fetch all the users, ordered by the oldest updated first
        """
        return [str(user_id[0]) for user_id in db_session.query(User.id)]

    def __repr__(self):
        return '<User {0}>'.format(self.id)
