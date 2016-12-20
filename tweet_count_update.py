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
Go through tweets, in batches of 100 and update their favourite and retweet counts
"""

def batch_ids():
    return [tweet.id for tweet in Tweet.batch_to_update()]


def update_tweet_counts():
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
            Tweet.update_counts(tweet.id, tweet.favorite_count, tweet.retweet_count)
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
            sys.stderr.write('[{}] Script tweet_count_update already running.\n'.format(time.strftime('%c')))
            sys.exit(-1)
        raise
    print('[{}] Start tweet_count_update'.format(time.strftime('%c')))
    update_tweet_counts()
