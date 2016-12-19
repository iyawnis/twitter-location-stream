from model import Tweet
import tweepy
from auth import auth_handler
import json


def batch_to_ids():
    batch = Tweet.batch_to_update()
    ids = [tweet.id for tweet in batch]
    print([(tw.id, tw.last_update) for tw in batch[0:1]])
    return ids

def get_ids_to_update():
    tweets_to_update = batch_to_ids()
    api = tweepy.API(auth_handler)
    if tweets_to_update:
        print('Updating tweets..', end="")
    while tweets_to_update:
        response = api.statuses_lookup(tweets_to_update, False, False)
        updated_tweets = set()
        for tweet in response:
            print('.', end="")
            Tweet.update_counts(tweet.id, tweet.favorite_count, tweet.retweet_count)
            updated_tweets.add(tweet.id)
        no_results = set(tweets_to_update) - updated_tweets
        if no_results:
            print('No results', no_results)
            for tweet_id in no_results:
                Tweet.bump_last_update(tweet_id)
            # Mark tweets that did not come back as updated, so we dont keep quering them
            # map(lambda x: Tweet.bump_last_update(x), no_results)
        tweets_to_update = batch_to_ids()

    print('')
    print('Finished updating tweets.')


if __name__ == '__main__':
    get_ids_to_update()
