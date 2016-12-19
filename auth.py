from tweepy import OAuthHandler


#Variables that contains the user credentials to access Twitter API 
consumer_key = "oM3MZdZBg7M6KO0UWKyFFsqSx"
consumer_secret = "bnAC76XUIhPbMInmT9cAtieXmVzs4DIj2F0yvGpBenzaVLFaah"
access_token = "802493452218986496-5UBID2TqvSKnaw1FQP97Ua6ZzgQcGBx"
access_token_secret = "2NYW1WEo8Yh3ld51gQoUls1Mz4m4gILlsrPvqq1orVqIm"


auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)