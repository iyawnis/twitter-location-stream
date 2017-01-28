from tweepy import OAuthHandler


#Variables that contains the user credentials to access Twitter API
# DO NOT SHARE
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)