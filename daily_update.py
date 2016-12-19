from model import Tweet
import tweepy
from auth import auth_handler
import json
import time


def batch_ids():
    return [tweet.id for tweet in Tweet.batch_to_update()]

def get_ids_to_update():
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
        no_results = set(tweets_to_update) - updated_tweets
        if no_results:
            # Mark tweets that did not come back as updated, so we dont keep quering them
            [Tweet.bump_last_update(tweet_id) for tweet_id in no_results]
            total_failed += len(no_results)

        tweets_to_update = batch_ids()
    end_time = time.time()
    print('')
    print('updated={} no_results={} time_elapsed={:.2f}'.format(total_updates, total_failed, (end_time - start_time)))


if __name__ == '__main__':
    print('Begin tweet counts update...')
    get_ids_to_update()
