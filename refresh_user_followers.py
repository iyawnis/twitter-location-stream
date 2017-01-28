#!/usr/bin/env python
import tweepy
import json
import time
import fcntl
import sys
import errno
from auth import auth_handler
from model import Tweet, User

"""
Go through tweets, in batches of 100 and update the stored data
"""
def create_new_users(existing_ids):
    print('Creating new users..')
    user_ids = [tweet.user_id for tweet in Tweet.fetch_distinct_users()]
    new_users = set(user_ids) - existing_ids
    User.batch_create(new_users)
    print('Created {} users'.format(len(new_users)))

def refresh_user_followers(create_new=False):
    existing_ids = set([user.id for user in User.fetch_users()])
    if create_new:
        create_new_users(existing_ids)
    api = tweepy.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    for user in User.fetch_users():
        followers_ids = []
        try:
            for page in tweepy.Cursor(api.followers_ids, user_id=user.id).pages():
                print('Found {} followers'.format(len(page)))
                followers_ids.extend(page)
            users_in_system = existing_ids & set(followers_ids)
            if users_in_system:
                User.update_followers(user.id, users_in_system)
                print('Updated followers for ', user.id, users_in_system)
        except tweepy.error.TweepError:
            print('Could not retrieve followers for {}'.format(user))
            continue

if __name__ == '__main__':
    f = open ('user_lock', 'w')
    try:
        fcntl.lockf (f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as e:
        if e.errno == errno.EAGAIN:
            sys.stderr.write('[{}] Script refresh_user_followers already running.\n'.format(time.strftime('%c')))
            sys.exit(-1)
        raise
    create_new = True if 'create' in sys.argv else False

    print('[{}] Start refresh_user_followers'.format(time.strftime('%c')))
    refresh_user_followers(create_new)
