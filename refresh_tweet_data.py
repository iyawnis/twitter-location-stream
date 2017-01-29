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
    """
     Get the tweet ids, for all the tweets that are due to be updated.
    """
    return [tweet.id for tweet in Tweet.batch_to_update()]

def refresh_tweet_replies():
    """
    Go through all Tweets in the database, and if one is a reply to
    existing tweet in the DB, increment its reply count
    """
    for tweet in Tweet.all_with_json():
        reply_to = tweet.json.get('in_reply_to_status_id')
        if reply_to is not None:
            print(reply_to, flush=True)
            Tweet.increment_replies(reply_to)


def refresh_tweet_data():
    """
    Fetch a list of tweet ids that are due to be updated, and request them
    from the Twitter API. Update the DB with the new results
    """
    tweets_to_update = batch_ids()
    api = tweepy.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    total_updates = 0
    total_failed = 0
    start_time = time.time()

    print('Updating tweets...', end="")
    while tweets_to_update:
        print('.', end='', flush=True)
        try:
            # statuses_lookup will return the current state of the requested tweets
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
            # Fetch the next batch
            tweets_to_update = batch_ids()
        except tweepy.error.TweepError as e:
            # API might return errors occasionally
            print_exc()
            time.sleep(30)
    end_time = time.time()
    print('')
    print('[{}] updated={} failed_update={} time_elapsed={:.2f}'.format(time.strftime('%c'), total_updates, total_failed, (end_time - start_time)))


if __name__ == '__main__':
    # File lock used when the script is run by a scheduler, to make sure we only
    # run the script once at a time
    f = open ('lock', 'w')
    try:
        fcntl.lockf (f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as e:
        if e.errno == errno.EAGAIN:
            sys.stderr.write('[{}] Script refresh_tweet_data already running.\n'.format(time.strftime('%c')))
            sys.exit(-1)
        raise

    if 'local' in sys.argv:
        print('[{}] Start refresh_tweet_replies'.format(time.strftime('%c')))
        refresh_tweet_replies()
    else:
        print('[{}] Start refresh_tweet_data'.format(time.strftime('%c')))
        refresh_tweet_data()
