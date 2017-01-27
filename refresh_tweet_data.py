#!/usr/bin/env python
import tweepy
import json
import time
import fcntl
import sys
import errno
from auth import auth_handler
from model import Tweet

"""
Go through tweets, in batches of 100 and update the stored data
"""

def batch_ids():
    return [tweet.id for tweet in Tweet.batch_to_update()]


def refresh_tweet_data():
    tweets_to_update = batch_ids()
    api = tweepy.API(auth_handler)
    total_updates = 0
    total_failed = 0
    start_time = time.time()

    if tweets_to_update:
        print('Updating tweets...', end="")
    while tweets_to_update:
        print('.', end="", flush=True)
        response = api.statuses_lookup(tweets_to_update, False, False)
        updated_tweets = set()
        for tweet in response:
            Tweet.update_data(tweet.id, tweet)
            updated_tweets.add(tweet.id)
            total_updates += 1
        failed_update = set(tweets_to_update) - updated_tweets
        if failed_update:
            # Mark tweets that did not come back as updated, so we dont keep quering them
            [Tweet.bump_last_update(tweet_id) for tweet_id in failed_update]
            total_failed += len(failed_update)

        tweets_to_update = batch_ids()
    end_time = time.time()
    print('')
    print('[{}] updated={} failed_update={} time_elapsed={:.2f}'.format(time.strftime('%c'), total_updates, total_failed, (end_time - start_time)))


if __name__ == '__main__':
    f = open ('lock', 'w')
    try:
        fcntl.lockf (f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as e:
        if e.errno == errno.EAGAIN:
            sys.stderr.write('[{}] Script refresh_tweet_data already running.\n'.format(time.strftime('%c')))
            sys.exit(-1)
        raise
    print('[{}] Start refresh_tweet_data'.format(time.strftime('%c')))
    refresh_tweet_data()
