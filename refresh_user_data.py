#!/usr/bin/env python
import tweepy
import json
import time
import fcntl
import sys
import errno
from auth import auth_handler
from model import Tweet, User

def create_new_users(existing_ids):
    """
    Find all unique users that have posted a tweet, and create an entry for them
    """
    print('Creating new users..')
    user_ids = [tweet.user_id for tweet in Tweet.fetch_distinct_users()]
    # Only create entires for users that dont already exist
    new_users = set(user_ids) - existing_ids
    User.batch_create(new_users)
    print('Created {} users'.format(len(new_users)))

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def refresh_user_followers():
    """
    Update the tweet counters for all users, then select the most popular users
    and update their counts
    """
    api = tweepy.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    all_users = User.fetch_users()
    update_count = 0
    print('[{}] Updating user counters..'.format(time.strftime('%c')))
    for user in all_users:
        update_count += 1
        aggregation_result = Tweet.get_user_tweet_counts(user.id)
        user.total_tweet_favourites = aggregation_result[0] or 0
        user.total_tweet_retweets = aggregation_result[1] or 0
        user.total_tweet_replies = aggregation_result[2] or 0
        user.tweet_count = aggregation_result[3] or 0
    User.save()  # We only commit the session once to speed things up

    print('[{}] Done'.format(time.strftime('%c')))
    print('[{}] Begin refreshing most popular users'.format(time.strftime('%c')))
    top_users = User.get_highest_counter_users()
    top_users = list(top_users)
    top_users.reverse()
    for user in top_users:
        user_follower_ids = []
        for page in tweepy.Cursor(api.followers_ids, user_id=user.id).pages():
            user_follower_ids.extend(page)
            print('[{}] Paginate... ({} followers)'.format(time.strftime('%c'), len(user_follower_ids)))
        User.update_followers(user.id, user_follower_ids)
        print('[{}] Updated followers for user: {}, followers: {}'.format(time.strftime('%c'), user.id, len(user_follower_ids)))
    print('[{}] Update complete.'.format(time.strftime('%c')))

def refresh_user_data(create_new=False):
    """
    Iterate through all our users, fetch their followers, and add any followers who
    are in the users table, in their list of followers
    """
    start_time = time.time()
    update_count = 0
    existing_ids = set([user.id for user in User.fetch_users()])
    if create_new:
        create_new_users(existing_ids)
    api = tweepy.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    print('Updating User data...', end='')
    for users_chunk in chunks(User.fetch_users(), 100):
        try:
            response = api.lookup_users([user.id for user in users_chunk])
            print('.', end='', flush=True)
            for user_json in response:
                update_count += 1
                User.update_data(user_json.id, user_json)
        except tweepy.error.TweepError:
            # API might return errors occasionally
            print_exc()
            time.sleep(30)
    end_time = time.time()
    print('')
    print('[{}] updated={} time_elapsed={:.2f}'.format(time.strftime('%c'), update_count, (end_time - start_time)))


if __name__ == '__main__':
    # File lock, only run the script once at a time
    f = open ('user_lock', 'w')
    try:
        fcntl.lockf (f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as e:
        if e.errno == errno.EAGAIN:
            sys.stderr.write('[{}] Script refresh_user_data already running.\n'.format(time.strftime('%c')))
            sys.exit(-1)
        raise
    # Create new flag tells the script if it should scan the tweet table for new users
    create_new = True if 'create' in sys.argv else False
    if 'update_followers' in sys.argv:
        print('[{}] Start refresh_user_followers'.format(time.strftime('%c')))
        refresh_user_followers()
    else:
        print('[{}] Start refresh_user_data'.format(time.strftime('%c')))
        refresh_user_data(create_new)
